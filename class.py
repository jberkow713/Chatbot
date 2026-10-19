import random 
class Nums:
    def __init__(self, low,high,count):
        self.low = low 
        self.high = high 
        self.count = count 
    def rand_return(self):
        return [random.randint(self.low,self.high) for _ in range(self.count)]
    def low_return(self):
        return [self.low for _ in range(self.count)]
    def high_return(self):
        return [self.high for _ in range(self.count)]
    def change_count(self,num):
        self.count = num 
    def avg_return(self):
        return [(self.high+self.low)/2 for _ in range(self.count)]
                   
n = Nums(1,10,10)
print(n.rand_return())
print(n.low_return())
n.change_count(20)
print(n.high_return())
n.change_count(5)
print(n.avg_return())   

def create_list_nums(count):
    return [((random.randint(0,10),random.randint(0,25), random.randint(0,25))) for _ in range(count)]

c = create_list_nums(10)
for x in c:
    print(x)
    n = Nums(*x)
    print(n.low_return())
    print(n.high_return())
