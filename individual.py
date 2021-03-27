from figures import get_random_figure
from config import INDIVIDUAL_SIZE
from tools.timer import MeasureTime
from tools.image import compare_images, Image, get_blank_image
from tools import check_chance
from config import SIZE
import os
import pickle
import datetime


class Individual:
    def __init__(self, target_image=None, figures=None):
        self.score = 0
        self.relevant_image = False
        self.__img = None
        self.target_image = target_image

        with MeasureTime('creating one gen', level='debug'):
            self.data = figures or [
                get_random_figure()
                for _ in range(INDIVIDUAL_SIZE)
            ]
    
    def fitness(self) -> float:
        """
        Return fitness value of individual
        """
        if not self.relevant_image:
            self.score = compare_images(self.img, self.target_image)

        return self.score

    @property
    def img(self):
        if not self.relevant_image:
            self.__img = self._get_full_image()
            self.relevant_image = True
        
        return self.__img

    def _get_full_image(self) -> Image.Image:
        """
        Return composed image of individual
        first images on foreground,
        last on background
        """
        canvas = get_blank_image(SIZE)
        for dna in reversed(self.data):
            canvas.alpha_composite(dna.img)
        
        return canvas
        
    def mutate(self, chance):
        """
        Inplace mutation of individual
        """
        if not check_chance(chance):
            return
        
        self.relevant_image = False
        with MeasureTime('mutation', level='debug'):
            for dna in self.data:
                dna.mutate()
    
    def cross(self, other):
        pass

    def save(self, output_dir):
        file_name = f"genetic-{datetime.datetime.now().strftime('%d_%H_%M_%S')}.pickle"
        output_file = os.path.join(output_dir, file_name)
        with open(output_file, 'wb') as file:
            pickle.dump(self, file)
    
    @staticmethod
    def load(file_path):
        with open(file_path, 'rb') as file:
            obj = pickle.load(file)

        return obj

    def __ge__(self, value):
        return self.score.__ge__(value.score)
    
    def __gt__(self, value):
        return self.score.__gt__(value.score)
    
    def __le__(self, value):
        return value.__ge__(self)
    
    def __lt__(self, value):
        return value.__gt__(self)