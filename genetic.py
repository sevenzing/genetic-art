from config import POPULATION_SIZE
from individual import Individual
from tools.timer import MeasureTime
from tools import parallelize_task, multiprocess_task


class Genetic:
    def __init__(self, target_image):
        self.target_image = target_image
        with MeasureTime('creating population'):
            args_list = [(target_image,) for _ in range(POPULATION_SIZE)]
            self.population = \
                parallelize_task(Individual, args_list)

    @property
    def best(self):
        return self.population[0]   

    def run(self):
        """
        Run genetic algorithm
        """
        self.best.save('output')

    def evaluate(self):
        """
        Evaluate the population
        """
        with MeasureTime('evaluate'):
            for individual in self.population:
                individual.fitness()


    def crossover(self, mode):
        """
        Crossover the population
        
        how ? 
        """

    def mutation(self, chance):
        """
        Mutate population
        """
        with MeasureTime('mutation'):
            args_list = [(ind, chance) for ind in self.population]
            parallelize_task(Individual.mutate, args_list)
    
    def select(self):
        """
        
        """