'''
Jackson Butler
Template for project usage and testing
Just replace self variables and change any functionality, while maintaining the same methods
'''


from modules.Population import Population
from modules.chord import Chord
from modules.helpers import output_to_midi
from statistics import mean
import json
import os


class Main:

    def __init__(self, 
                 runs=1, 
                 generations=30, 
                 popSize:int=20, 
                 genotypeLength:int=4, 
                 pTransformMutation:float=0.33, 
                 pNoteTransformMutation:float=0.5,
                 pTimeMutation:float=0.5, 
                 pTransformCross:float=0.5, 
                 pTimeCross:float=0.5, 
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
        
        self.generations = generations
        self.runs = runs

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
        self.stringHeader = f'Fitness Equation: {self._fitnessType}\n| gen |          best genotype         | fitness |         worst genotype         | fitness |  mean | stdev |\n'

        self.curRun = 1
        self.curGeneration = 0
        self._curPopulation = None
        self._tempGenotypes = []

        # Stat Tracking
        self._fitnessResults = []

    def _update_stats(self):
        """
        Updates self._fitnessResults
        Returns:
            None: None
        """
        results = self._curPopulation.results
        self._fitnessResults.append((results[0], results[1], results[2], results[3]))
        
    def save_generation_stats_to_file(self, filePath):
        """
        Not currently used
        
        Args:
            filePath (str): defined in __name__ == "__main__"
        """
        if self.curGeneration == 0:  # only writes header if first iteration
            with open(filePath,"w") as file:
                file.writelines(self.stringHeader)
        else:
            with open(filePath,"a") as file:
                file.writelines(f"| {self.curGeneration:3} {self._curPopulation}\n")
        
    def save_run_stats_to_file(self, filePath):
        """
        Writes averages of averages from each run to given filePath

        Args:
            filePath (str): defined in __name__ == "__main__"
        """
        bestFitness = mean([individual[0] for individual in self._fitnessResults])
        worstFitness = mean([individual[1] for individual in self._fitnessResults])
        avgPopFitness = mean([individual[2] for individual in self._fitnessResults])
        avgStDev = mean([individual[3] for individual in self._fitnessResults])
        
        with open(filePath,"a") as file:
            if self.curRun == 1:
                file.writelines(f"| Best Fitness Avg | Worst Fitness Avg | Avg Population Fitness | Avg Standard Deviation |\n")
            file.writelines(f"| {bestFitness:.3f} | {worstFitness:.3f} | {avgPopFitness:.3f} | {avgStDev:.3f} |\n")
            if self.curRun == self.runs:
                file.writelines("\n")
        
    def save_population_to_file(self, filePath):
        """ Helper function for UI """
        jsonObject = json.dumps(self._curPopulation.genotypes if isinstance(self._curPopulation,Population) else self._curPopulation , indent=4)
        with open(filePath, 'w') as file:
            file.write(jsonObject)

    def load_population_from_file(self, filePath):
        """ Helper function for UI """
        with open(filePath, 'r') as file:
            population = json.load(file)
            self._curPopulation = population
        if isinstance(self._curPopulation,list):
            self.load_population_from_self(loadPop=True)

    
    def update_params(self, newParams):
        """ Helper funciton for UI """
        self._genotypeLength = newParams["genotypeLength"]
        self._pTransformMutation = newParams["pTransformMutation"]
        self._pNoteTransformMutation = newParams["pNoteTransformMutation"]
        self._pTimeMutation = newParams["pTimeMutation"]
        self._pTransformCross = newParams["pTransformCross"]
        self._timeMutationRange = newParams["timeMutationRange"]
        self._isMelody = newParams["isMelody"]
        self.generations = newParams["generations"]
        self.runs = newParams["runs"]
        self._fitnessType = newParams["fitnessType"]
        self._s = newParams["s"]
        self.curRun = newParams["curRun"]
        self.curGeneration = newParams["curGeneration"]
        self.stringHeader = f'Fitness Equation: {self._fitnessType}\n| gen |          best genotype         | fitness |         worst genotype         | fitness |  mean | stdev |\n'
        if self._curPopulation != None:
            self.load_population_from_self(loadPop=True)


    def get_params(self):
        """ Helper function for UI """
        return {
            "popSize":self._popSize, 
            "genotypeLength":self._genotypeLength, 
            "pTransformMutation":self._pTransformMutation, 
            "pNoteTransformMutation":self._pNoteTransformMutation,
            "pTimeMutation":self._pTimeMutation, 
            "pTransformCross":self._pTransformCross, 
            "pTimeCross":self._pTimeCross, 
            "timeMutationRange":self._timeMutationRange, 
            "isMelody":self._isMelody,
            "fitnessType":self._fitnessType,
            "s":self._s,
            "generations":self.generations,
            "runs":self.runs,
            "curRun":self.curRun,
            "curGeneration":self.curGeneration
        }
    
    def save_params_to_file(self, newParams, filePath):
        jsonObject = json.dumps(newParams, indent=4)
        with open(filePath, 'w') as file:
            file.write(jsonObject)

    def load_params_from_file(self, filePath):
        """ Helper function for UI """
        with open(filePath, 'r') as file:
            newParams = json.load(file)
            self._popSize = newParams["popSize"]
            self._genotypeLength = newParams["genotypeLength"]
            self._pTransformMutation = newParams["pTransformMutation"]
            self._pNoteTransformMutation = newParams["pNoteTransformMutation"]
            self._pTimeMutation = newParams["pTimeMutation"]
            self._pTransformCross = newParams["pTransformCross"]
            print(newParams["timeMutationRange"], type(newParams["timeMutationRange"]) )
            
            self._timeMutationRange = tuple(newParams["timeMutationRange"].strip(" ").split(","))
            self._isMelody = newParams["isMelody"]
            self.generations = newParams["generations"]
            self.runs = newParams["runs"]
            self._fitnessType = newParams["fitnessType"]
            self._s = newParams["s"]
            self.curRun = newParams["curRun"]
            self.curGeneration = newParams["curGeneration"]
    
    def load_population_from_self(self, genPop=False, loadPop=False):
        """ Helper function for UI """
        if loadPop:
            print("load")
            self._curPopulation = Population(self._popSize, 
                                             self._genotypeLength, 
                                             self._pTransformMutation, 
                                             self._pNoteTransformMutation, 
                                             self._pTimeMutation, 
                                             self._pTransformCross, 
                                             self._pTimeCross, 
                                             timeMutationRange=self._timeMutationRange,
                                             isMelody=self._isMelody, 
                                             chord=self._chord, 
                                             chords=self._chords, 
                                             bestIndividuals=self._bestIndividuals, 
                                             genPopulation=genPop, 
                                             loadFromGenotype=(self._curPopulation.genotypes if isinstance(self._curPopulation,Population) else self._curPopulation if isinstance(self._curPopulation,list) else None), 
                                             fitnessType=self._fitnessType, s=self._s)
        else:
            print("gen")
            self._curPopulation = Population(self._popSize, self._genotypeLength, self._pTransformMutation, self._pNoteTransformMutation, self._pTimeMutation, self._pTransformCross, self._pTimeCross, timeMutationRange=self._timeMutationRange, isMelody=self._isMelody, chord=self._chord, chords=self._chords, bestIndividuals=self._bestIndividuals, genPopulation=genPop, fitnessType=self._fitnessType, s=self._s)
    
    def run(self, writeToFile=False, filePath=None):
        """iterates until all runs and generations have occured"""
        
        while self.curGeneration < (self.generations*(self.runs)) or self.generations == 0:  # if 0 generations run infinitely
            
            self.curGeneration += 1
            
            if self._curPopulation == None:  # generate new population
                
                self.load_population_from_self(genPop=True)
                
            else:  # next generation
                
                self._curPopulation = self._curPopulation.next_generation(self.generations, self.curGeneration)

            self._update_stats()
            
            self._curPopulation.save_measure(self._curPopulation.population[-1])
            yield self._curPopulation
            
            if self.runs > 1 and (self.curGeneration % self.generations == 0 and self.generations != 0):  # if not infinite or if generation num has been reached
                
                if writeToFile:
                    
                    self.save_run_stats_to_file(filePath)
                    
                # Reset population values if generations has been reached
                self._fitnessResults = []
                self._curPopulation = None
                self.curRun += 1
                print('end Run')            

if __name__ == "__main__":
    # File Path Definitions
    dataDir = os.path.abspath("versions/base_evolutionary_algorithm/data/")
    populationFileName = "saved_population.json"
    
    runStatsFileName = "run_stats.txt"
    runStatsFilePath = os.path.join(dataDir, runStatsFileName)
    
    question4 = Main(runs=1, generations=10, popSize=20, genotypeLength=2, pTransformMutation=0.33, pNoteTransformMutation=0.7, pTimeMutation=0.5,  pTransformCross=0.5, pTimeCross=0.5, fitnessType=0, s=1.5, genPopulation=True)
    for i in question4.run(True, runStatsFilePath):
        print(i, i.maxFitness)


    # # Questions from homework
    # question1 = Main(runs=20, generations=100, base=2, bitLength=30, popSize=100, pMutation=1/30, pCross=0.7, noOfCrossPoints=1, fitnessType=0)
    # for i in question1.run(True, runStatsFilePath):
    #     pass
    
    # question2 = Main(runs=20, generations=100, base=2, bitLength=30, popSize=100, pMutation=1/30, pCross=0.7, noOfCrossPoints=2,  fitnessType=0)
    # for i in question2.run(True, runStatsFilePath):
    #     pass
    
    # question3 = Main(runs=20, generations=100, base=2, bitLength=30, popSize=100, pMutation=1/30, pCross=0.7, noOfCrossPoints=5, fitnessType=0)
    # for i in question3.run(True, runStatsFilePath):
    #     pass
    
    # question4 = Main(runs=20, generations=100, base=2, bitLength=30, popSize=100, pMutation=1/30, pCross=0.7, noOfCrossPoints=10, fitnessType=0)
    # for i in question4.run(True, runStatsFilePath):
    #     pass
    
    
    """
    It seems as though the number of crossing points causes no significant changes to the performance of the algorithm.
    All runs are very quite equivelent with no outliers present.
    """