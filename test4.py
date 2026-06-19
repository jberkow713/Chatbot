import random 
def empty_list(size,l=None,count=0):
    if count == 0:
       l = [random.randint(0,100) for _ in range(size)] 
    if len(l)==0:
        return l 
    l.pop(0)
    count+=1
    print(l) 
    return empty_list(size,l,count)

empty_list(10)       