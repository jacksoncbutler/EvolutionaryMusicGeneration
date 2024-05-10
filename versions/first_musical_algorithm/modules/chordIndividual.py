'''
Jackson Butler
Pledged
Contains a class for the individual of a population
'''


import random
from .helpers import get_translations, generate_chord_genotype, crossover
import copy

class chordIndividual:
    
    def __init__(self, genotype:list, pTransformMutation:float, pNoteTransformMutation:float , pTimeMutation:float, parents:tuple=('None', 'None'), isMelody:bool=False):
        self._genotype = genotype  # changed to list (2d array)
        """
        [
            ['R','L','H'],  # Transformations
            [1,1,1,],       # Time
        ]
        """
        self._pTransformMutation = pTransformMutation
        self._pNoteTransformMutation = pNoteTransformMutation
        self._pTimeMutation = pTimeMutation
        self._parents = parents
        self._fitnessPercentage = 0
        self.fitness = 0
        self._isMelody = isMelody

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
        genotypeTime            = [random.randrange(*timeMutationRange)/100 if random.random() <= self._pTimeMutation else self._genotype[1][i] for i in range(len(self._genotype[1]))]


        # if self._isMelody:
        #     middleTransform = []
        #     middleTime = []
        #     if random.random() <= 0.5:
        #         for index in range(len(genotypeTransformation)):
        #             if random.random() <= self._pNoteTransformMutation:
        #                 middleTransform.append(random.choice(possibleTransformations))
        #                 middleTime.append(random.randrange(*timeMutationRange)/100)

        #             middleTransform.append(genotypeTransformation[index])
        #             middleTime.append(genotypeTransformation[index])
        #     else:
        #         for index in range(len(genotypeTransformation)):
        #             if random.random() > self._pNoteTransformMutation:
        #                 middleTransform.append(genotypeTransformation[index])
        #                 middleTime.append(genotypeTransformation[index])
            
        #     genotypeTransformation = middleTransform
        #     genotypeTime = middleTime

            
        # Need to do something about this INTEGER or FLOAT

        self._genotype[0] = genotypeTransformation
        self._genotype[1] = genotypeTime

    def __str__(self):
        return f'{self.genotype}'
                
    
if __name__ == '__main__':
    # Minor test code
    indi = chordIndividual([['R','P','L'],[1,1,1]], 0.5, 0.5 )
    indi.mutate()
    print(indi.genotype)

    print('\n––––––––––––––––––––––––––––––––')
    
    indi1 = chordIndividual(generate_chord_genotype(3,4), 0.5, 0.1,)
    indi2 = chordIndividual(generate_chord_genotype(8,3), 0.5, 0.1,)
    print(indi1)
    print(indi2)
    print(crossover(indi1.genotype, indi2.genotype))
    