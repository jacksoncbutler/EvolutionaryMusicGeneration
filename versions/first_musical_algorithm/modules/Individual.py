'''
Jackson Butler
Pledged
Contains a class for the individual of a population
'''


import random
from chord import Chord

class Individual:

    translate = {'R':'R', 'P':'P', 'L':'L', 'H':'PLP', 'S':'LPR', 'N':'RLP', 'F':'LR', 'M':'RL'}
    
    def __init__(self, genotype:list, base:int, pMutation, parents:tuple=('None', 'None')):
        self._base = base
        self._genotype = genotype  # changed to list (2d array)
        """
        [
            ['R','L','H'],  # Transformations
            [1,1,1,],       # Time
        ]
        """
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
    
    # @property
    # def phenotype(self):
    #     """
    #     Returns bit string genotype as an int
    #     """
    #     return int(self._genotype, self._base)
    
    def mutate(self):  # need to rewrite this to accomadate for new list Genotype
        """
        Tries to mutate each bit in genotype
        This method only runs on creation of Individual
        """

        # Mutate Transformations
        possibleTransformations = list(Individual.translate.keys())

        genotypeTransformation  = [random.choice(possibleTransformations) if random.random() <= self._pMutation else self._genotype[0][i] for i in range(len(self._genotype[0]))]
        genotypeTime            = [random.randrange(0,400)/100 if random.random() <= self._pMutation else self._genotype[1][i] for i in range(len(self._genotype[1]))]

        self._genotype[0] = genotypeTransformation
        self._genotype[1] = genotypeTime
                

    
    
if __name__ == '__main__':
    # Minor test code
    chord = Chord()
    indi = Individual([['R','P','L'], [1, 1, 1,]], base=2, pMutation=0.5)
    indi.mutate()
    # print(indi.genotype)

    chord.fill_operations(indi.genotype[0])

    chord.perform_operations()
    print(())
    indi.mutate()
    # print("geno:",indi.genotype)

    chord.fill_operations(indi.genotype[0])

    chord.perform_operations()
    