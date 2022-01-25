DROP TABLE IF EXISTS list;
DROP TABLE IF EXISTS task;

CREATE TABLE list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    list_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    completed BOOL NOT NULL,
    FOREIGN KEY (list_id) REFERENCES lists (id)
);
  
