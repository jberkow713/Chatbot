import random
import collections
from collections import deque 
def create_matrix(rows,cols):
    c = [[random.randint(0,1) for _ in range(rows)] for _ in range(cols)]
    return c

M = (create_matrix(5,5))

def num_islands(matrix):
    if not matrix:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    islands = 0

    def bfs(r,c):
        q = collections.deque()
        visited.add((r,c))
        q.append((r,c))

        while q:
            # take item out of the list at element 0 to feed into the algorithm
            row,col = q.popleft()
            dirs = [(1,0),(-1,0),(0,1), (0,-1)]
            for dr, dc in dirs:
                R,C = row +dr, col+dc
                if R >=0 and R<rows and C>=0 and C<cols:
                    if matrix[R][C]==1 and (R,C) not in visited:
                        q.append((R,C))
                        visited.add((R,C))
        
        return 1
    for r in range(rows):
        for c in range(cols):
            pos = matrix[r][c]
            if pos == 1 and (r,c) not in visited:
                islands+=bfs(r,c)
                

    return islands             

for x in M:
    print(x)
print(num_islands(M))


