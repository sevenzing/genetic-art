from config import POPULATION_SIZE, INDIVIDUAL_SIZE, ITERS, MUTATION_CHACE, OUTPUT_DIR, PORTION_OF_MUTATION
from individual import Individual
from tools.timer import MeasureTime
from tools import parallelize_task, create_dir
from tools.image import show_image
from random import randint
from typing import List
from os import urandom
from os.path import join
import logging


class Genetic:
    def __init__(self, target_image):
        self._id = urandom(4).hex().zfill(8)
        self.target_image = target_image
        self.size = POPULATION_SIZE

        logging.warning(f"Starting genetic alg with id {self._id}")
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
            prev_score = 1024
            mutation_chance = MUTATION_CHACE
            portion_of_mutation = PORTION_OF_MUTATION

            for iterNumber in range(ITERS):
                with MeasureTime('one iter', level='info'):
                    if iterNumber % 100 == 0:
                        best = self.best
                        worse = self.worse
                        title = f"#{iterNumber}. best is {best.score}, worse is {worse.score}"
                        logging.warning(title)
                        if show_img:
                            show_image(best.img, title)
                            directory = join(OUTPUT_DIR, self._id)
                            create_dir(directory)
                            best.img.save(join(directory, f"{iterNumber // 100}.png"))

                        delta = best.score - prev_score
                        prev_score = best.score
                        if delta > 1024 * 0.001:
                            mutation_chance += 0.05
                            portion_of_mutation = max(portion_of_mutation - 0.001, 0.005)
                            logging.warning(f"Delta is {delta}. New chance: {mutation_chance}, share: {portion_of_mutation}")


                    self.evaluate()
                    self.population.sort()

                    new_population = self.crossover()
                    self.select()
                    self.population.extend(new_population)
                    self.size = len(self.population)
                    
                    assert self.size == POPULATION_SIZE
                    
                    self.mutation(mutation_chance, portion_of_mutation)

            
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

    def mutation(self, chance, share):
        """
        Mutate population
        """
        with MeasureTime('mutation'):
            args_list = [(ind, chance, int(INDIVIDUAL_SIZE * share)) for ind in self.population]
            parallelize_task(Individual.mutate, args_list)
    
    def select(self):
        """
        Remove half of the population

        Assume that self.population is sorted
        """

        save_index = int(self.size * 3 / 8)
        with MeasureTime('select'):
            while self.size > POPULATION_SIZE//2:
                index_to_remove = randint(save_index + 1, self.size - 1)
                individual = self.population.pop(index_to_remove)
                del individual
                self.size -= 1
            
        
        