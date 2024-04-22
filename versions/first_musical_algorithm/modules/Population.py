'''
Jackson Butler
Pledged
Contains a class for the population of a genetic algorithm
'''


from Individual import Individual
from helpers import crossover, random_binary_string, normalize
from statistics import mean, stdev
import random
import math


class Population:
    
    def __init__(self, base:int, bitLength:int, popSize:int, pMutation:float, pCross:float, noOfCrossPoints:int, fitnessEq:str, genPopulation:bool=False, loadFromGenotype=None, fitnessType:int=0, s=1.5):
        self._base = base
        self._bitLength = bitLength
        self._popSize = popSize
        self._pMutation = pMutation
        self._pCross = pCross
        self._noOfCrossPoints = noOfCrossPoints
        self._fitnessType = fitnessType
        self._s = s
        self._fitnessEq = fitnessEq
        self._fitnessSum = float(0)
        self._fitnessWheel = []

        self.population = []
        # Generates a population of popSize length if genPopulation
        if genPopulation or isinstance(loadFromGenotype, list): self.gen_population(loadFromGenotype)
            
    
    def __str__(self):
        """
        Returns best performing bitString in the current generation in string format
        return: str
        """
        # genotype, phenotype, normalPhenotype, fitness, worstGenotype,  = self.results
        return '| {} | {:10} | {:16f} | {:.5f} | {} | {:.5f} | {:.3f} | {:.3f} |'.format(*self.results)
    
    def gen_population(self, genotypes = None):
        if isinstance(genotypes, list):
            for individual in genotypes:
                self.populate_Population(individual, mutate=False)
        else:
            for _ in range(self._popSize):  
                self.populate_Population(random_binary_string(self._bitLength, self._base), mutate=False)
        self.evaluate_fitness()
    

    def populate_Population(self, individual, mutate=True, parent1=None, parent2=None):
        """
        Args:
            individual (_type_): _description_
            mutate (bool, optional): _description_. Defaults to True.
            parent1 (_type_, optional): _description_. Defaults to None.
            parent2 (_type_, optional): _description_. Defaults to None.
        """
        individual = Individual(individual, self._base, self._pMutation, (parent1,parent2))
        if mutate: individual.mutate()
        individual.fitness = self.evaluate(individual)
        self.population.append(individual)

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
    
    def next_generation(self):
        """
        Creates new population
        Roulette Wheel then generates children of selected parents newPopulation
        return: class Population
        """
        newPopulation = Population(self._base, self._bitLength, self._popSize, self._pMutation, self._pCross, self._noOfCrossPoints, self._fitnessEq, fitnessType=self._fitnessType, s=self._s)

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

            if random.random() <= self._pCross:  # Tries to cross parents
                children = crossover(individual1.genotype, individual2.genotype, self._noOfCrossPoints)
            else:  # Make children that are copies of each respective parent
                children = (individual1.genotype, individual2.genotype)
            
            for child in children:
                newPopulation.populate_Population(child, True, individual1, individual2)  # Adds each child to the population
                
        newPopulation.evaluate_fitness()

        return newPopulation
            
    def evaluate(self, individual):
        """
        input: individual of type individual
        Evaluates fitness equation with normalized phenotype
        Then adds resulting fitness value to self._fitnessSum
        return: fitness of type float
        """
        fitness = eval(
            self._fitnessEq,
            globals(),
            {'z': normalize(individual.phenotype, (self._base**self._bitLength)-1)},
        )
        self._fitnessSum += fitness
        return fitness
        
    
if __name__ == '__main__':
    # Basic test code, for more in depth testing use the test.py file

    generations = 50
    pop = Population(base=2, bitLength=30, popSize=30, pMutation=0.0333, pCross=0.6, fitnessEq='z**10', noOfCrossPoints=1, genPopulation=True)
    print(pop)
    genCount = 1
    while genCount < generations:
        pop = pop.next_generation()
        print(pop)
        genCount += 1
    
    
    
    