from config import POPULATION_SIZE
from individual import Individual
from tools.timer import MeasureTime


class Genetic:
    def __init__(self):
        with MeasureTime('creating population'):
            self.population = [
                Individual()
                for _ in range(POPULATION_SIZE)
            ]
    

    def run(self):
        """
        Run genetic algorithm
        """

    def evaluate(self):
        """
        Evaluate the population
        """
        

    def crossover(self, mode):
        """
        Crossover the population
        
        how ? 
        """

    def mutation(self, chance):
        """
        Mutate population
        """
        for individual in self.population:
            individual.mutate(chance)
    
    def select(self):
        """
        
        """