'''
Jackson Butler
Pledged
Contains useful helper functions for use in genetic algorithms
'''

import copy
import random
# from individual import Individual

def crossover(genotype1:list, genotype2:list):

    for section in range(len(genotype1)):
        diff = len(genotype1[section]) - len(genotype2[section])
        # print('section',genotype1[section])
       

        if diff > 0:
            crossingPoint = random.randrange(len(genotype2))
            tempGeno = copy.deepcopy(genotype1)
            diff = abs(diff)

            
            genotype1[section] = [*(tempGeno[section][:crossingPoint+diff]), *(genotype2[section][crossingPoint:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint]), *(tempGeno[section][crossingPoint+diff:])]


        elif diff < 0:
            crossingPoint = random.randrange(len(genotype1))
            tempGeno = copy.deepcopy(genotype1)
            diff = abs(diff)


            genotype1[section] = [*(tempGeno[section][:crossingPoint]), *(genotype2[section][crossingPoint+diff:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint+diff]), *(tempGeno[section][crossingPoint:])]

        else:
            crossingPoint = random.randrange(len(genotype1))
            tempGeno = copy.deepcopy(genotype1)

            genotype1[section] = [*(tempGeno[section][:crossingPoint]), *(genotype2[section][crossingPoint:])]
            genotype2[section] = [*(genotype2[section][:crossingPoint]), *(tempGeno[section][crossingPoint:])]

    
    return genotype1, genotype2


def get_translations():
    return {'R':'R', 'P':'P', 'L':'L', 'H':'PLP', 'S':'LPR', 'N':'RLP', 'F':'LR', 'M':'RL'}

def generate_genotype(length:int, maxFloat:int=4) -> list:
    return [random_transformations_list(length), random_integer_list(length, maxFloat)]


def random_integer_list(length:int, base:int=9) -> list:
    # random.seed(42)
    return [random.randrange(0,base) for _ in range(length)]

def random_float_list(length:int, max:int) -> list:
    # random.seed(42)
    return [round(random.randrange(0,max*100) / 100, 1) for _ in range(length)]

def random_transformations_list(length:int) -> list:
    # random.seed(42)
    keys = list(get_translations().keys())
    return [random.choice(keys) for _ in range(length)]


def normalize(number:int, total): 
    return float(number/(total))


if __name__ == '__main__':
    print(get_translations()['N'])
    print(random_transformations_list(4))
    print(random_integer_list(4, 10))

    


    