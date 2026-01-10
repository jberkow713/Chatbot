import copy 

def subseq(word,lst):
    # word = 'abcde'
    # lst = ['ab','bb',ce']
    # output how many words in this list can exist in the word, 
    # with the ability to remove characters, so 'ace' would be found, but 'acb' would not
    # order of letters matters

    val = list(enumerate(word))
    d = {}
    
    for idx,l in val:
        d[idx]=l 
    D = {}
    for k,v in d.items():
        if v not in D:
            D[v]=[k] 
        else:
            D[v].append(k)
    # D = {'a': [0], 'b': [1, 5], 'c': [2], 'd': [3], 'e': [4, 6]}
    # creates dictionary where each key is a letter and each value are the indexes in order where that value
    # appears in the word

    # iterate through the words, with count starting at 0
    count = 0
    
    for val in lst:
        found = True 
        # set initial found = True , and disqualify based on loop
        # each iteration, copy the original dictionary, because values will be removed from list each time
        # a letter is found in order
        E = copy.deepcopy(D)
        cur = -1 
        print(E)
        for l in val:
            if l not in E:
                # if the letter is not in the dictionary, word can not exist
                print('not found',l)
                found = False 

            else:
                if len(E[l])>0:
                    # if the length of the remaining indexes for the given letter is >0, 
                    # iterate through remaining values and 
                    # check to see if any of the values are greater than the cur value, if so set cur= value
                    # remove value from the list, and break the loop
                    bigger = False 
                    for IDX in E[l]:
                        
                        if IDX > cur:
                            print(IDX)
                            cur = IDX 
                            E[l].remove(IDX)
                            bigger = True 
                        
                        if bigger ==True:
                            break 

                    if bigger == False:
                        # if a letter exists, but is not in the right order, this will trigger
                        found = False 
                else:
                    # if the letter has an empty list, it has already been used, and can not be
                    # in the current word
                    found = False
                    print(val)
                    
                     
            if found ==False:
                # at any point, if this is triggered, break from the word, do not increment the count
                break

        if found ==True:
            print(val)
            count +=1

    return count      

            
import string 
import random 
s = string.ascii_lowercase[:10]

c = [''.join([random.choice(s) for _ in range(3)]) for _ in range(5) ]
word = ''.join([random.choice(s) for _ in range(15)])
print(c)
print(subseq(word,c))