'''
Jackson Butler
Pledged
Contains a class for the individual of a population
'''


import random
from helpers import get_translations, generate_genotype, crossover

class Individual:
    
    def __init__(self, genotype:list, pTransformMutation:float, pTimeMutation:float, parents:tuple=('None', 'None')):
        self._genotype = genotype  # changed to list (2d array)
        """
        [
            ['R','L','H'],  # Transformations
            [1,1,1,],       # Time
        ]
        """
        self._pTransformMutation = pTransformMutation
        self._pTimeMutation = pTimeMutation
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
    def transforms(self):
        """
        Returns outerscope readonly genotype
        """
        return self._genotype[0]
    
    @property
    def times(self):
        """
        Returns bit string genotype as an int
        """
        return self._genotype[1]
    
    def mutate(self, timeMutationRange:tuple):  # need to rewrite this to accomadate for new list Genotype
        """
        Tries to mutate each bit in genotype
        This method only runs on creation of Individual
        """

        # Mutate Transformations
        possibleTransformations = list(get_translations().keys())
        genotypeTransformation  = [random.choice(possibleTransformations) if random.random() <= self._pTransformMutation else self._genotype[0][i] for i in range(len(self._genotype[0]))]

        # Need to do something about this INTEGER or FLOAT
        genotypeTime            = [random.randrange(*timeMutationRange)/100 if random.random() <= self._pTimeMutation else self._genotype[1][i] for i in range(len(self._genotype[1]))]

        self._genotype[0] = genotypeTransformation
        self._genotype[1] = genotypeTime

    def __str__(self):
        return f'{self.genotype}'
                
    
if __name__ == '__main__':
    # Minor test code
    indi = Individual([['R','P','L'],[1,1,1]], 0.5, 0.5 )
    indi.mutate()
    print(indi.genotype)

    print('\n––––––––––––––––––––––––––––––––')
    
    indi1 = Individual(generate_genotype(3,4), 0.5, 0.1,)
    indi2 = Individual(generate_genotype(8,3), 0.5, 0.1,)
    print(indi1)
    print(indi2)
    print(crossover(indi1.genotype, indi2.genotype))
    