'''
Jackson Butler
Pledged
Contains a class for the individual of a population
'''


import random


class Individual:
    
    def __init__(self, genotype:list, base:int, pMutation, parents:tuple=('None', 'None')):
        self._base = base
        self._genotype = genotype  # changed to list (2d array)
        self._pMutation = pMutation
        self._parents = parents
        self._fitnessPercentage = 0
        self.fitness = 0


    @property
    def genotype(self):
        """
        Returns outerscope readonly genotype
        """
        return self._genotype
    
    @property
    def phenotype(self):
        """
        Returns bit string genotype as an int
        """
        return int(self._genotype, self._base)
    
    def mutate(self):  # need to rewrite this to accomadate for new list Genotype
        """
        Tries to mutate each bit in genotype
        This method only runs on creation of Individual
        """
        # self._genotype = ''.join(
        #     [str(int(not(int(self._genotype[mutationPoint]))))  # inverted point appended to list if below statement is true
        #         if random.random() <= self._pMutation else self._genotype[mutationPoint]  # if random value is within mutation range ^, else append same value to list
        #         for mutationPoint in range(len(self._genotype)) # iterate through length of genotyope
        #     ]
        # )
        

        self._genotype = ''.join(
            [str(random.randrange(0,self._base))  # inverted point appended to list if below statement is true
                if random.random() <= self._pMutation else self._genotype[mutationPoint]  # if random value is within mutation range ^, else append same value to list
                for mutationPoint in range(len(self._genotype)) # iterate through length of genotyope
            ]
        )
    
    
if __name__ == '__main__':
    # Minor test code
    indi = Individual('0011101')
    indi.mutate(0.1)
    print(indi.genotype)
 
    