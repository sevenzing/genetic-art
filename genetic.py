from config import POPULATION_SIZE, INDIVIDUAL_SIZE, ITERS, MUTATION_CHACE, OUTPUT_DIR
from individual import Individual
from tools.timer import MeasureTime
from tools import parallelize_task, multiprocess_task
from typing import List
from random import randint
import logging


class Genetic:
    def __init__(self, target_image):
        self.target_image = target_image
        self.size = POPULATION_SIZE

        with MeasureTime('creating population'):
            args_list = [(target_image,) for _ in range(self.size)]
            self.population = \
                parallelize_task(Individual, args_list)

    @property
    def best(self):
        return self.population[0]   
    
    @property
    def worse(self):
        return self.population[-1]

    def run(self, show_img=True):
        """
        Run genetic algorithm
        """
        try:
            for iterNumber in range(ITERS):
                with MeasureTime('one iter', level='info'):
                    if iterNumber % 100 == 0:
                        best = self.best
                        worse = self.worse
                        logging.warning(f"#{iterNumber}. best is {best.score}, worse is {worse.score}")
                        if show_img:
                            best.img.show()

                    self.evaluate()
                    self.population.sort(reverse=True)

                    new_population = self.crossover()
                    self.select()
                    self.population.extend(new_population)
                    self.size = len(self.population)
                    
                    self.mutation(MUTATION_CHACE)

                    assert self.size == POPULATION_SIZE
            
            self.best.save(OUTPUT_DIR)
        except KeyboardInterrupt as e:
            self.best.save(OUTPUT_DIR)
            raise e

    def evaluate(self):
        """
        Evaluate the population
        """
        

    def crossover(self) -> List[Individual]:
        """
        Crossover the population
        """
        
        assert self.size % 2 == 0
        with MeasureTime('crossover'):
            new_individuals = [
                self.population[i].cross(self.population[self.size - i - 1])
                for i in range(self.size // 2)
            ]

        return new_individuals

    def mutation(self, chance):
        """
        Mutate population
        """
        with MeasureTime('mutation'):
            args_list = [(ind, chance, int(INDIVIDUAL_SIZE * 0.1)) for ind in self.population]
            parallelize_task(Individual.mutate, args_list)
    
    def select(self):
        """
        Remove half of the population
        """

        save_index = int(self.size * 3 / 8)
        with MeasureTime('select'):
            while self.size > POPULATION_SIZE//2:
                index_to_remove = randint(save_index + 1, self.size - 1)
                individual = self.population.pop(index_to_remove)
                del individual
                self.size -= 1
            
        
        