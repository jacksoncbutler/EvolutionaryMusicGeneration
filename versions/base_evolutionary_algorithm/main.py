'''
Jackson Butler
Template for project usage and testing
Just replace self variables and change any functionality, while maintaining the same methods
'''


from modules.Population import Population
from statistics import mean
import json
import os


class Main:

    def __init__(self, runs=1, generations=30, base=2, bitLength=30, popSize=50, pMutation=0.0333, pCross=0.6, noOfCrossPoints=1, fitnessEq="z**10", fitnessType=0, s=1.5):
        self._base = base
        self._bitLength = bitLength
        self._popSize = popSize
        self._pMutation = pMutation
        self._pCross = pCross
        self._noOfCrossPoints = noOfCrossPoints
        self._fitnessEq = fitnessEq
        self.generations = generations
        self.runs = runs
        self._fitnessType = fitnessType
        self._s = s
        self.stringHeader = f'Fitness Equation: {self._fitnessEq}, {self._fitnessType}\n| gen |          best genotype         |  phenotype | normal phenotype | fitness |         worst genotype         | fitness |  mean | stdev |\n'

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
        self._fitnessResults.append((results[3], results[5], results[6], results[7]))
        
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
        
    def save_population_to_file(self, newParams, filePath):
        """ Helper function for UI """
        jsonObject = json.dumps(newParams, indent=4)
        with open(filePath, 'w') as file:
            file.write(jsonObject)

    def load_population_from_file(self, filePath):
        """ Helper function for UI """
        with open(filePath, 'r') as file:
            newParams = json.load(file)
            self._base = newParams["base"]
            self._bitLength = newParams["bitLength"]
            self._popSize = newParams["popSize"]
            self._pMutation = newParams["pMutation"]
            self._pCross = newParams["pCross"]
            self._noOfCrossPoints = newParams["noOfCrossPoints"]
            self._fitnessEq = newParams["fitnessEq"]
            self.generations = newParams["generations"]
            self.runs = newParams["runs"]
            self._fitnessType = newParams["fitnessType"]
            self._s = newParams["s"]
            self.curRun = newParams["curRun"]
            self.curGeneration = newParams["curGeneration"]
    
    def update_params(self, newParams):
        """ Helper funciton for UI """
        self._base = newParams["base"]
        self._bitLength = newParams["bitLength"]
        self._popSize = newParams["popSize"]
        self._pMutation = newParams["pMutation"]
        self._pCross = newParams["pCross"]
        self._noOfCrossPoints = newParams["noOfCrossPoints"]
        self._fitnessEq = newParams["fitnessEq"]
        self.generations = newParams["generations"]
        self.runs = newParams["runs"]
        self._fitnessType = newParams["fitnessType"]
        self._s = newParams["s"]
        self.curRun = newParams["curRun"]
        self.curGeneration = newParams["curGeneration"]
        self.stringHeader = f'Fitness Equation: {self._fitnessEq}, {self._fitnessType}\n| gen |          best genotype         |  phenotype | normal phenotype | fitness |         worst genotype         | fitness |  mean | stdev |\n'
        if self._curPopulation != None:
            self.load_population_from_self(loadPop=True)

    def get_params(self):
        """ Helper function for UI """
        return {
            "base":self._base,
            "bitLength":self._bitLength,
            "popSize":self._popSize,
            "pMutation":self._pMutation,
            "pCross":self._pCross,
            "noOfCrossPoints":self._noOfCrossPoints,
            "fitnessEq":self._fitnessEq,
            "fitnessType":self._fitnessType,
            "s":self._s,
            "generations":self.generations,
            "runs":self.runs,
            "curRun":self.curRun,
            "curGeneration":self.curGeneration
        }
    
    def load_population_from_self(self, genPop=False, loadPop=False):
        """ Helper function for UI """
        if loadPop:
            print("load")
            self._curPopulation = Population(self._base, self._bitLength, self._popSize, self._pMutation, self._pCross, self._noOfCrossPoints, self._fitnessEq, genPopulation=genPop, loadFromGenotype=self._curPopulation.genotypes, fitnessType=self._fitnessType, s=self._s)
        else:
            print("gen")
            self._curPopulation = Population(self._base, self._bitLength, self._popSize, self._pMutation, self._pCross, self._noOfCrossPoints, self._fitnessEq, genPopulation=genPop, fitnessType=self._fitnessType, s=self._s)
    
    def run(self, writeToFile=False, filePath=None):
        """iterates until all runs and generations have occured"""
        
        while self.curGeneration < (self.generations*(self.runs)) or self.generations == 0:  # if 0 generations run infinitely
            
            self.curGeneration += 1
            
            if self._curPopulation == None:  # generate new population
                
                self.load_population_from_self(genPop=True)
                
            else:  # next generation
                
                self._curPopulation = self._curPopulation.next_generation()

            self._update_stats()
            
            yield self._curPopulation
            
            if self.runs > 1 and (self.curGeneration % self.generations == 0 and self.generations != 0):  # if not infinite or if generation num has been reached
                
                if writeToFile:
                    
                    self.save_run_stats_to_file(filePath)
                    
                # Reset population values if generations has been reached
                self._fitnessResults = []
                self._curPopulation = None
                self.curRun += 1
            

if __name__ == "__main__":
    # File Path Definitions
    dataDir = os.path.abspath("versions/base_evolutionary_algorithm/data/")
    populationFileName = "saved_population.json"
    
    runStatsFileName = "run_stats.txt"
    runStatsFilePath = os.path.join(dataDir, runStatsFileName)
    
    question4 = Main(runs=1, generations=100, base=2, bitLength=30, popSize=100, pMutation=1/30, pCross=0.7, noOfCrossPoints=1, fitnessType=0)
    for i in question4.run(True, runStatsFilePath):
        print(i)

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