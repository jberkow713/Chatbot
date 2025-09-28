import random

def enum_dict(top,num):
    D= {}
    for idx,val in list(enumerate([random.randint(0,top) for _ in range(num)])):
        D[idx]=val
    print(D)  
    return D 

def find_sorted_dict(D):
    sorted_items = sorted(D.items(), key=lambda item: item[1])
    a = [x[1] for x in sorted_items]
    b = [x[0] for x in sorted_items]
    return b,a[0],b[0]

def find_sorted_random_keys(top,num):
    d = enum_dict(top,num)
    return find_sorted_dict(d)

# print(find_sorted_random_keys(10000,1000))


class dog_enum:
    def __init__(self, top,num,name):
        self.top = top 
        self.num = num 
        self.ordered_keys,self.smallest,self.smallest_key = find_sorted_random_keys(self.top,self.num)
        self.name = name
        
    def bark(self):
        print(f'Ruff Ruff, I am {self.name}, smallest key is {self.smallest_key}, with a value of {self.smallest}')    


d = dog_enum(100,100,'Roger')
d.bark()