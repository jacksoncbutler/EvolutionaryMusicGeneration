'''
Jackson Butler
Pledged
Contains a class for the population of a genetic algorithm
'''


from individual import Individual
from helpers import crossover, generate_genotype, normalize
from statistics import mean, stdev
from chord import Chord
import random
import math


class Population:
    
    def __init__(self,popSize:int, genotypeLength:int, maxNoteLength:int, pTransformMutation:float, pTimeMutation:float, pTransformCross:float, pTimeCross:float, fitnessEq:str, genPopulation:bool=False, loadFromGenotype=None, fitnessType:int=0, s=1.5, chord=Chord(), chords=[]):
        
        # self._bitLength = bitLength # This can now change

        self._popSize = popSize

        self._genotypeLength = genotypeLength
        self._maxNoteLength  = maxNoteLength


        self._pTransformMutation = pTransformMutation
        self._pTimeMutation = pTimeMutation

        self._pTransformCross = pTransformCross
        self._pTimeCross = pTimeCross

        self._fitnessType = fitnessType
        self._s = s
        self._fitnessEq = fitnessEq

        self._fitnessSum = float(0)
        self._fitnessWheel = []

        self._chord  = chord
        self._chords = chords

        self.population = []

        # Generates a population of popSize length if genPopulation
        if genPopulation or isinstance(loadFromGenotype, list): self.gen_population(loadFromGenotype)
            
    
    def __str__(self):
        """
        Returns best performing bitString in the current generation in string format
        return: str
        """
        # genotype, phenotype, normalPhenotype, fitness, worstGenotype,  = self.results
        results = self.results
        return ' | {} | {} | {} | {} |'.format(*results)
    

    def gen_population(self, genotypes = None):

        if isinstance(genotypes, list):
            for individual in genotypes:
                self.populate_Population(individual, mutate=False)

        else:

            for _ in range(self._popSize):  
                self.populate_Population(generate_genotype(self._genotypeLength, self._maxNoteLength), mutate=False)
        self.evaluate_fitness()
    

    def populate_Population(self, genotype, mutate=True, parent1=None, parent2=None):
        """
        Args:
            individual (_type_): _description_
            mutate (bool, optional): _description_. Defaults to True.
            parent1 (_type_, optional): _description_. Defaults to None.
            parent2 (_type_, optional): _description_. Defaults to None.
        """
        individual = Individual(genotype, self._pTransformMutation, self._pTimeMutation, (parent1,parent2))
        if mutate: individual.mutate()
        individual.fitness = self.evaluate(individual)

        self.population.append(individual)

    def evaluate(self, individual):
        """
        input: individual of type individual
        Evaluates fitness equation with normalized phenotype
        Then adds resulting fitness value to self._fitnessSum
        return: fitness of type float
        """
        # fitness = eval(
        #     self._fitnessEq,
        #     globals(),
        #     {'z': normalize(individual.phenotype, (self._base**self._bitLength)-1)},
        # )
        fitness = random.random() # temporary
        self._fitnessSum += fitness
        return fitness

    def evaluate_fitness(self):
        """
        Creates roulette wheel
        """
        normalizedSum = 0
        self.population.sort(key=lambda x:x.fitness) # Not required, just for nice looking output.
        
        if self._fitnessType == 2:
            expoSum = sum([( self._s * ( ( 1 - self._s )**( self._popSize-individualRank-1))) for individualRank in range(self._popSize)])

        elif self._fitnessType == 3:
            expoSum = sum([1-(math.e**(-individualRank) ) for individualRank in range(self._popSize)])

        for individualRank in range(len(self.population)):

            individual = self.population[individualRank]
            individual
            if self._fitnessType == 0:
                """Fitness Ranking"""
                normalizedSum += normalize(individual.fitness, self._fitnessSum)
                
            elif self._fitnessType == 1:
                """Linear Ranking"""
                normalizedSum += ( ( 2 - self._s ) / self._popSize ) + \
                                ( ( ( 2 * individualRank ) * ( self._s - 1) ) / ( self._popSize * ( self._popSize - 1))) 
                  
            elif self._fitnessType == 2:
                """Exponential Ranking"""
                normalizedSum += ( self._s * ( ( 1 - self._s )**( self._popSize-individualRank-1)))/expoSum
                
            self._fitnessWheel.append(normalizedSum)

            
        count = -1
        self._chord.fill_operations(self.population[-1].transforms)
        self.population[-1].transforms
        for chord in self._chord.perform_operations():
            count += 1
            self._chords.append((chord, self.population[-1].times[count]))

    def next_generation(self):
        """
        Creates new population
        Roulette Wheel then generates children of selected parents newPopulation
        return: class Population
        """
        newPopulation = Population(self._popSize, self._genotypeLength, self._maxNoteLength, self._pTransformMutation, self._pTimeMutation, self._pTransformCross, self._pTimeCross, self._fitnessEq, fitnessType=self._fitnessType, s=self._s, chord=self._chord, chords=self._chords)

        # Select Parents (roulette wheel)
        while len(newPopulation.population) < self._popSize:  # Fill new population
            ''' 
            (This is the actual selection from the roulette wheel)
            Turn this into a function that allows for variable number of parents
            And takes away the repitition of code
            This is more efficient than the function will likely be depending on how I write it though
            '''
            individual1 = random.random()  # Random value for use in selection wheel
            individual2 = random.random()  # Random value for use in selection wheel
            
            for index in range(len(self._fitnessWheel)):  # Iterates through fitness wheel ranges
                fitnessValue = self._fitnessWheel[index]

                if not isinstance(individual1, Individual):  # Check if individual is not a member of a class
                    if individual1 <= fitnessValue:  # Check if random value is within current fitness range
                        individual1 = self.population[index]

                if not isinstance(individual2, Individual):  # Check if individual is not a member of a class

                    if individual2 <= fitnessValue:  # Check if random value is within current fitness range
                        individual2 = self.population[index]

            if random.random() <= self._pTransformCross:  # Tries to cross parents
                children = crossover(individual1.genotype, individual2.genotype)
            else:  # Make children that are copies of each respective parent
                children = (individual1.genotype, individual2.genotype)
            
            for child in children:
                newPopulation.populate_Population(child, True, individual1, individual2)  # Adds each child to the population
                
        newPopulation.evaluate_fitness()

        return newPopulation
    
    @property
    def results(self):
        """
        Returns best performing bitString in the current generation as a list
        return: list
        """
        return (self.population[-1].genotype, self.population[-1].fitness, self.population[0].genotype, self.population[0].fitness)


    
        
    
if __name__ == '__main__':
    # Basic test code, for more in depth testing use the test.py file

    generations = 10
    pop = Population(100, 4 ,4,0.25, 0.25, 0.5, 0.5, fitnessEq='z**10', genPopulation=True)
    print(pop)
    genCount = 1
    while genCount < generations:
        pop = pop.next_generation()
        # print(pop)
        # print(pop._chords[-4:])
        genCount += 1
    
    print(pop._chords)
    
    
    