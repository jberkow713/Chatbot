# import torch
# import tensorflow as tf 
import numpy as np 

# v = np.array([3,1])

# class hi:
#     def __init__(self, name):
#         self.name = name 
#     def hello(self):
#         return f"Hello {self.name}"    

# h = hi("james")
# print(h.hello())
import random 
A = [random.randint(0,10) for _ in range(10)]

def find_first_last(arr,val):
    if val not in arr:
        return False
    l = list(enumerate(arr))
    d  = {}
    for idx,val in l:
        if val not in d:
            d[val]=[idx]
        else:
            d[val].append(idx)


    print(d,val)

    if val not in d:
        return False 
    elif val in d:
        if len(d[val])==1:
            return d[val][0],d[val][0]
        else:
            return d[val][0], d[val][-1]                   

# print(find_first_last(A,4))


def find_max(Lst):
    curr = Lst[0]
    Lst = Lst[1:]
    for i in range(len(Lst)):
        if Lst[i]>curr:
            curr = Lst[i]
    return curr 

def find_nth_largest(Lst, n):
    largest = []
    for i in range(n):
        c = find_max(Lst)
        Lst.remove(c)
        largest.append(c)
    print(largest)    
    return largest[-1]


def calc_sum_lowest_2(L):
    print(L)
    if len(L)<2:
        return None 
    s = sorted(L)
    return s[0]+s[1]    

B = [random.randint(0,10) for _ in range(10)]
print(B)
print(find_nth_largest(A,9))
print(calc_sum_lowest_2(B))

class Dog:
    def __init__(self, name, age):
        self.name = name 
        self.age = age
        self.kids = []
    def bark(self):
        for i in range(1,self.age+1):
            print(f'I am {i} years old')
    def de_age(self, years):
        if type(years)!=int:
            print('years must be integer')
            return 
        self.age = self.age -years
        self.bark()
    def make_puppy(self, name):
        d = Puppy(name,self.name)
        print(d)
        d.bark()
        self.kids.append(d)
        return d  
class Puppy:
    def __init__(self, name,creator):
        self.name  = name
        self.creator = creator 
    def __repr__(self):
        return(f"Puppy's name is {self.name}")
    def bark(self):
        print(f'{self.name} barks gleefully for his parent {self.creator}')
class Puppy_Factory:
    def __init__(self, dog_list):
        self.dog_list = dog_list
        self.create_puppies()
    def create_puppies(self):
        Dog_Puppies = {}

        for info in self.dog_list:
            puppy_name = info[2]
            D = Dog(info[0], info[1])
            Dog_Puppies[D]= D.make_puppy(puppy_name)

        return Dog_Puppies
d = Dog('Danny',25)
d.bark()
d.de_age(10)
d.make_puppy('Brian Griffin')                

p = Puppy_Factory([('Brad', 10, 'Fred'),('James',8,'Mike')])

