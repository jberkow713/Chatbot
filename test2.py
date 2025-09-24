import random

def enum_dict(top,num):
    D= {}
    for idx,val in list(enumerate([random.randint(0,top) for _ in range(num)])):
        D[idx]=val
    return D 


def find_sorted_dict(D):
    sorted_items = sorted(D.items(), key=lambda item: item[1])
    print([x[1] for x in sorted_items])
    return [x[0] for x in sorted_items]

def find_sorted_random_keys(top,num):
    d = enum_dict(top,num)
    
    return find_sorted_dict(d)

print(find_sorted_random_keys(1000,10))
