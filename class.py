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

                   
n = Nums(1,10,10)
print(n.rand_return())
print(n.low_return())
n.change_count(20)
print(n.high_return())        