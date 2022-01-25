#!/usr/bin/env python3
import sys
import sqlite3
from flask import Flask, request, jsonify, g
from flask_cors import CORS
DATABASE = 'todo.db'
app = Flask(__name__)
cors = CORS(app)

def init_tables():
    with sqlite3.connect("todo.db") as conn:
        with open('schema.sql') as f:
            conn.executescript(f.read())
            conn.commit()
    print("database initiated!")

def conv_to_dicts(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = conv_to_dicts
    return db

def query_db(query, args=()):
    cur = get_db().cursor()
    cur.execute(query, args)
    data = cur.fetchall()
    get_db().commit()
    cur.close()
    return data, cur.lastrowid

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def list_error(id):
    ids, __ = query_db("SELECT id from list")
    ids = [v['id'] for v in ids]
    if id in ids:
        return None
    else:
        return jsonify({
            'status': 'error',
            'info': 'List with id={} does not exist!'.format(id)
        })

def task_error(list_id, task_id):
    task_ids, __ = query_db(
        "SELECT id FROM task WHERE list_id = ?",
        (list_id,)
    )
    print(task_ids,list_id)
    task_ids = [v['id'] for v in task_ids]
    print(task_id,task_ids)
    if task_id > len(task_ids)-1 or task_id <= 0:
        return True, jsonify({
            'status': 'error',
            'info': 'Task with id={} does not exist in list with id={}!'.format(
                task_id, list_id)
        })
    elif task_id > 0:
        return False, task_ids[task_id - 1]

def insert_list(data):
    for list_ in data:
        sql = 'INSERT INTO list (name) VALUES (?)'
        __, id = query_db(sql, (list_.get('name', ''),))
        insert_task(list_.get('tasks',[]), id)

def update_list(data, id):
    sql = 'UPDATE list SET name = ? WHERE id = ?'
    query_db(sql, (data.get('name', ''), id))

def delete_list(id=None):
    if id:
        query_db('DELETE FROM list  WHERE id = ?', (id,))
    else:
        query_db('DELETE FROM list')

def get_list(id=None):
    if id:
        lists_, __ = query_db("SELECT * FROM list WHERE id == ?;", (id,))
    else:
        lists_, __ = query_db("SELECT * FROM list")
    tasks, __ = query_db("SELECT * FROM task;")
    data = []
    for list_ in lists_:
        data.append({
            'name': list_['name'],
            'tasks': [
                {k: v for k, v in task.items() if 'id' not in k} 
                for task in tasks if task['list_id'] == list_['id']
            ]
        })
    return jsonify(data[0] if len(data) == 1 else data)

def insert_task(data, list_id):
    for task in data:
        sql = "INSERT INTO task ({}, list_id) VALUES ({})".format(
            ','.join(list(task.keys())),
            ','.join(['?']*4)
        )
        query_db(sql, tuple(task.values()) + (list_id,))

def update_task(data, list_id, task_id):
    sql = 'UPDATE task SET {} WHERE id = ? AND list_id =?'.format(
        ' = ?, '.join(list(data.keys()))+' = ?',
    )
    data, __ = query_db(sql, tuple(data.values()) + (task_id, list_id))

def delete_task(**id):
    if id:
        query_db(
            "DELETE FROM task WHERE {} = ?".format(list(id.keys())[0]),
            tuple(id.values())
        )

def get_task(**id):
    if id:
        tasks, __ = query_db(
            "SELECT * FROM task where {} = ?".format(list(id.keys())[0]),
            tuple(id.values())
        )
    return jsonify(tasks[0] if len(tasks) == 1 else tasks)


@app.route(
    "/lists/<int:list_id>",
    methods=['GET', 'PUT', 'DELETE'])
def handle_list(list_id):
    if error := list_error(list_id):
        return error
    if request.method == 'PUT':
        update_list(request.json, list_id)
        task_ids, __ = query_db("SELECT id FROM task WHERE list_id == ?", (list_id,))
        task_ids = [v['id'] for v in task_ids]
        for i, task in enumerate(request.json.get('tasks',[])):
            if i > len(task_ids) - 1:
                return jsonify({
                    'status': 'error',
                    'info': 'Excessive tasks were not processed!'
                })
            else:
                update_task(task, list_id, task_ids[i])
        return jsonify({'status': 'success'})
    elif request.method == 'DELETE':
        delete_list(list_id)
        delete_task(list_id=list_id)
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return get_list(list_id)

@app.route(
    "/lists",
    methods=['POST', 'GET', 'DELETE'])
def handle_lists():
    if request.method == 'POST':
        insert_list(request.json)
        return jsonify({'status': 'success'})
    elif request.method == 'DELETE':
        delete_list()
        return jsonify({'status': 'success'})
    elif request.method == 'GET':
        return get_list()

@app.route(
    "/lists/<int:list_id>/tasks",
    methods=['POST', 'GET', 'DELETE'])
def handle_tasks(list_id):
    if error := list_error(list_id):
        return error
    if request.method == 'POST':
        insert_task(request.json, list_id)
        return jsonify({'status':'success'})
    elif request.method == 'DELETE':
        delete_task(list_id=list_id)
        return jsonify({'status':'success'})
    elif request.method == 'GET':
        return get_task(list_id=list_id)


@app.route(
    "/lists/<int:list_id>/tasks/<int:task_id>",
    methods=['GET', 'PUT', 'DELETE'])
def handle_task(list_id, task_id):
    print("handle: ",list_id, task_id)
    if error := list_error(list_id):
        return error
    error, result = task_error(list_id, task_id)
    if error:
        return result
    if request.method == 'PUT':
        update_task(request.json, list_id, result)
        return jsonify({'status':'success'})
    elif request.method == 'DELETE':
        delete_task(id=result)
        return jsonify({'status':'success'})
    elif request.method == 'GET':
        return get_task(id=result)

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1]:
        init_tables()
    app.run(host='192.168.1.16', port='5000')
