import { from, Observable} from 'rxjs';
import { filter, map, mergeMap} from 'rxjs/operators';
const persons$ = from([
    {
        id: 1,
        name: "Jan Kowalski"
    }, {
        id: 2,
        name: "John Doe"
    }, {
        id: 3,
        name: "Jarek Kaczka"
    }
])

const ages$ = from([
    {
        person: 1,
        age: 18
    }, {
        person: 2,
        age: 24
    }, {
        person: 3,
        age: 666
    }
]);

const locations$ = from([
    {
        person: 1,
        country: "Poland"
    }, {
        person: 3,
        country: "Poland"
    }, {
        person: 2,
        country: "USA"
    }
]);
const filtered = locations$.pipe(
    mergeMap(x => ages$.pipe(
        map(y => {
            if (y.person === x.person & x.country === "Poland"){
            return y.age
            }
        }))
        
    ),
    filter(age => age>0)
)
let age_sum = 0
let people = 0
let avg_age = 0
const age_sub = filtered.subscribe(v => {
    age_sum += v
    people++
    avg_age = age_sum/people
})
console.log("average age of people ligin in Poland is: ",avg_age)



