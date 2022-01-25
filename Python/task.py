#!/usr/bin/env python3
users = [
    {'name':'Kamil', 'country':'Poland'},
    {'name':'John', 'country':'USA'},
    {'name':'Yeti'}]
users_from_poland = [
    user for user in users if user.get('country','') == 'Poland']
print(users_from_poland)

########################

numbers = [
    1,5,2,3,1,4,1,23,12,2,3,1,2,
    31,23,1,2,3,1,23,1,2,3,123]
nr_sum = sum(numbers[5:15])
print(nr_sum)

########################

powers = [2**(i+1) for i in range(20)]
print(powers)