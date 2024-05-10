'''
Jackson Butler
Pledged
Contains a class for the population of a genetic algorithm
'''


from .chordIndividual import chordIndividual
from .melodyIndividual import melodyIndividual
from .helpers import crossover, generate_chord_genotype, normalize, output_to_midi, play_midi
from statistics import mean, stdev
from .chord import Chord
import copy
import random
import math


class Population:
    
    def __init__(self,popSize:int, 
                 genotypeLength:int, 
                 pTransformMutation:float, 
                 pNoteTransformMutation:float,
                 pTimeMutation:float, 
                 pTransformCross:float, 
                 pTimeCross:float, 
                 bestChord=None,
                 timeMutationRange:tuple=(200, 301), 
                 isMelody:bool=False,
                 genPopulation:bool=False, 
                 loadFromGenotype=None, 
                 fitnessType:int=0, 
                 s=1.5, 
                 chord=Chord(), 
                 chords=[], 
                 midiChords=[], 
                 bestIndividuals=[],):
        
        # self._bitLength = bitLength # This can now change

        self._popSize = popSize

        self._genotypeLength = genotypeLength


        self._pTransformMutation = pTransformMutation
        self._pNoteTransformMutation = pNoteTransformMutation
        self._pTimeMutation = pTimeMutation
        self._timeMutationRange = timeMutationRange

        self._pTransformCross = pTransformCross
        self._pTimeCross = pTimeCross

        self._fitnessType = fitnessType
        self._s = s

        self.maxFitness = 0
        self._fitnessSum = float(0)
        self._fitnessWheel = []

        self._isMelody = isMelody
        self._chord  = chord
        self._chords = chords
        self._midiChords = midiChords
        self._bestIndividuals = bestIndividuals
        # self._measureLength = measureLength

        self.population = []

        # Generates a population of popSize length if genPopulation
        if genPopulation or isinstance(loadFromGenotype, list): self.gen_population(loadFromGenotype, bestChord)
            
    
    
    def __str__(self):
        """
        Returns best performing bitString in the current generation in string format
        return: str
        """
        # genotype, phenotype, normalPhenotype, fitness, worstGenotype,  = self.results
        results = self.results
        return ' | {} | {} | {} | {} |'.format(*results)
    

    def gen_population(self, bestChord=None, genotypes = None):

        if isinstance(genotypes, list):
            for individual in genotypes:
                self.populate_Population(individual, bestChord, mutate=False,)

        else:

            for _ in range(self._popSize):
                if self._isMelody:
                    self.populate_Population(generate_chord_genotype(self._genotypeLength, self._timeMutationRange), bestChord, mutate=False)
                else:
                    self.populate_Population(generate_chord_genotype(self._genotypeLength, self._timeMutationRange), bestChord, mutate=False)
        self.evaluate_fitness()
    

    def populate_Population(self, genotype, bestChord=None, mutate=True, parent1=None, parent2=None, totalGenerations=100, currentGen=1):
        """
        Args:
            individual (_type_): _description_
            mutate (bool, optional): _description_. Defaults to True.
            parent1 (_type_, optional): _description_. Defaults to None.
            parent2 (_type_, optional): _description_. Defaults to None.
        """
        if self._isMelody:
            individual = melodyIndividual(genotype, self._pTransformMutation, self._pNoteTransformMutation, self._pTimeMutation, (parent1,parent2), self._isMelody)
        else:
            individual = chordIndividual(genotype, self._pTransformMutation, self._pNoteTransformMutation, self._pTimeMutation, (parent1,parent2), self._isMelody)
        if mutate: individual.mutate(self._timeMutationRange)
        individual.fitness = self.evaluate(individual, totalGenerations, currentGen, bestChord)

        self.population.append(individual)

    def evaluate(self, individual:chordIndividual|melodyIndividual, totalGenerations, currentGen, bestChord=None):
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
        # individual.transforms
        # fitness = random.random() # temporary

        # individual._genotype = [['N','S','R','S'], [1,1,1,1]]
        self.maxFitness = 0
        fitness = 0

        prevChord = copy.deepcopy(self._chord)
        testChord = copy.deepcopy(prevChord)
        prevChord:Chord
        testChord:Chord

        if len(self._midiChords) > 0:
            prevTime = self._midiChords[-1][1]
        else: prevTime = 0
        
        currentSongProgress = (currentGen/totalGenerations)*100
        simpleTransforms = Chord().test_fill(individual.transforms, self._isMelody)

        testChord.fill_operations(individual.transforms, self._isMelody)


        chords = []
        # print(testChord.perform_operations(self._isMelody))
        for chord in testChord.perform_operations(self._isMelody):
            chords.append(copy.deepcopy(chord))

        # if self._isMelody:
        
        # else:
        for index in range(len(individual.transforms,)):
            transform     = simpleTransforms[index]
            # print(chords)
            currentChord  = chords[index]
            currentChord:Chord
            time          = individual.times[index]
            
            # print(individual.transforms[index])
            
            if prevChord.is_tonic:
                if currentChord.is_tonic or currentChord.is_subDominant:
                    fitness += 100
            elif prevChord.is_subDominant:
                if currentChord.is_subDominant or currentChord.is_tonic:
                    fitness += 100
            elif prevChord.is_dominant:
                if currentChord.is_dominant or currentChord.is_tonic:
                    fitness += 100       

            # if str(individual.transforms[index]) in [*individual.transforms[:index], *individual.transforms[index+1:]]:
            #     fitness -= 50

            # var = min(((100*(currentSongProgress**2)) / ((1/20)*(currentSongProgress**3))) - 20, 33) 
            # # print(var)
            # if len(transform) > 1: fitness += 15
            # else:
            #     fitness += 33 - var

            # print(individual.times)
            # print(time)
            # print(type(individual), individual), 
            if time%0.25 == 0: 
                fitness += 30;
            # else: print(False)

            self.maxFitness +=  100 + 30

            prevChord = currentChord
            prevTime = time
        

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


    def save_measure(self, measure, midi=[]):
        count = 0
        self._chord.fill_operations(measure.transforms, self._isMelody)
        tempChords = []
        for chord in self._chord.perform_operations(self._isMelody):
            tempChords.append((chord.as_midi(), measure.times[count]))
            self._chords.append(copy.deepcopy(chord))
            count += 1
        # print(tempChords)
        self._midiChords.append(tempChords)
        # midi.append(tempChords)
        # print(self._midiChords[-1])
        self._bestIndividuals.append(measure)

        # return midi


    def next_generation(self, totalGenerations, currentGen, bestChord=None):
        """
        Creates new population
        Roulette Wheel then generates children of selected parents newPopulation
        return: class Population
        """

        newPopulation = Population(self._popSize, self._genotypeLength, self._pTransformMutation, self._pNoteTransformMutation, self._pTimeMutation, self._pTransformCross, self._pTimeCross, bestChord=bestChord, isMelody=self._isMelody, fitnessType=self._fitnessType, s=self._s, chord=self._chord, chords=self._chords, bestIndividuals=self._bestIndividuals)

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

                if not (isinstance(individual1, chordIndividual) or isinstance(individual1, melodyIndividual)):  # Check if individual is not a member of a class
                    if individual1 <= fitnessValue:  # Check if random value is within current fitness range
                        individual1 = self.population[index]

                if not (isinstance(individual2, chordIndividual) or isinstance(individual2, melodyIndividual)):  # Check if individual is not a member of a class

                    if individual2 <= fitnessValue:  # Check if random value is within current fitness range
                        individual2 = self.population[index]

            if random.random() <= self._pTransformCross:  # Tries to cross parents
                children = crossover(individual1.genotype, individual2.genotype)
            else:  # Make children that are copies of each respective parent
                children = (individual1.genotype, individual2.genotype)
            
            for child in children:
                newPopulation.populate_Population(child, True, individual1, individual2, totalGenerations, currentGen)  # Adds each child to the population
        
        newPopulation.evaluate_fitness()

        return newPopulation
    
    @property
    def results(self):
        """
        Returns best performing bitString in the current generation as a list
        return: list
        """
        return (self.population[-1].genotype, self.population[-1].fitness, self.population[0].genotype, self.population[0].fitness)
    
    @property
    def genotypes(self):
        genotypes = []
        for individual in self.population:
            genotypes.append(individual.genotype)
        return genotypes

    @property
    def chords(self):
        return self._chords
    
        
    
if __name__ == '__main__':
    # Basic test code, for more in depth testing use the test.py file
    chordMidi = []
    melodyMidi = []

    generations = 20
    chordsPop = Population(20, 2 ,1,0.33, 0.7, 0.5, 0.5, 0.5, fitnessType=0, s=1.5, genPopulation=True)
    # chordMidi = chordsPop.save_measure(chordsPop.population[-1], chordMidi)
    chordsPop.save_measure(chordsPop.population[-1])

    melodyPop = Population(30, 4 ,1,0.33, 0.7, 0.5, 0.5, 0.5, bestChord=chordsPop.population[-1], timeMutationRange=(50,125), fitnessType=2, s=1.5, genPopulation=True, isMelody=True)
    # melodyMidi = melodyPop.save_measure(melodyPop.population[-1], melodyMidi)
    melodyPop.save_measure(melodyPop.population[-1])


    # print(chordsPop._midiChords)
    # print(melodyPop._midiChords)
    # print('\n',chordsPop.population[-1],'\n')
    genCount = 1
    while genCount < generations:
        chordsPop = chordsPop.next_generation(generations, genCount,)
        # chordMidi = chordsPop.save_measure(chordsPop.population[-1], chordMidi)
        chordsPop.save_measure(chordsPop.population[-1])

        melodyPop = melodyPop.next_generation(generations, genCount, chordsPop.population[-1])
        # melodyMidi = melodyPop.save_measure(melodyPop.population[-1], melodyMidi)
        melodyPop.save_measure(melodyPop.population[-1])

        print('chords:',chordsPop)
        print('Melody:',melodyPop)

        # print([str(chord) for chord in pop._chords[-4:]])
        genCount += 1
    print("Chord maxFitness:", chordsPop.maxFitness)
    # print(chordsPop._midiChords)

    print("Melody maxFitness:", melodyPop.maxFitness)
    # print('last best item',melodyPop.population[-1])

    # midiChords = [chordsPop._midiChords[index] for index in range(0, len(chordsPop._midiChords), 2)]
    # midiMelody = [melodyPop._midiChords[index] for index in range(1, len(melodyPop._midiChords), 2)]
    # print(midiChords,'\n\n')
    # print(midiMelody)

    # output_to_midi(chordsPop._midiChords, melodyPop._midiChords, "midi_file.mid")
    output_to_midi(chordsPop._midiChords, melodyPop._midiChords, "midi_file.mid")
    # output_to_midi(chordMidi, melodyMidi, "midi_file.mid")
    play_midi("midi_file.mid")
    
    
    