'''
Jackson Butler
Pledged
Contains useful helper functions for use in genetic algorithms
'''

from http.client import MULTI_STATUS
import random

def crossover(parent1:str, parent2:str, noOfCrossPoints:int):
    
    if len(parent1) == len(parent2):
        if noOfCrossPoints <= len(parent1)-1:
            
            crossingPoints = sorted([*random.sample(range(0,len(parent1)-1),noOfCrossPoints), len(parent1)])
            child1 = ''
            child2 = ''
            prev = 0

            for crossingIndex in range(len(crossingPoints)):
                
                crossingPoint = crossingPoints[crossingIndex]
                
                if crossingIndex % 2 == 0:
                    
                    child1 += parent1[prev:crossingPoint]
                    child2 += parent2[prev:crossingPoint]
                    
                else:
                    
                    child1 += parent2[prev:crossingPoint]
                    child2 += parent1[prev:crossingPoint]
                    
                prev = crossingPoint
            
        else:
            raise ValueError("noOfCrossPoints exceeds the length of input strings")
    else:
        raise ValueError("Parent1 and Parent2 muse be of the same length")
    
    return child1, child2

def random_binary_string(length:int, base:int) -> list:
    # random.seed(42)
    return ''.join([str(random.randrange(0,base)) for _ in range(length)])

def normalize(number:int, total):
    return float(number/(total))



if __name__ == '__main__':
    pass
    