import datetime
import logging
import os
import pickle
from random import randint, sample
from PIL.Image import Image

from config import numpy as np

from config import DNA_IMAGE_SIZE, INDIVIDUAL_SIZE, OUTPUT_DIR, SIZE
from figures import Figure
from tools import check_chance, get_all_files, create_dir
from tools.image import (Image, get_blank_image, image_fitness_pixel_by_pixel,
                         low_image)
from tools.timer import MeasureTime


class Individual:
    def __init__(self, target_image: Image, figures=None, score=None):
        self.relevant_image = False
        self.__img = None
        self.target_image = target_image

        with MeasureTime('creating one gen', level='debug'):
            if figures:
                self.figures = figures
            else:
                self.figures = []
                for i in range(INDIVIDUAL_SIZE):
                    x1 = (i % (SIZE[0]//DNA_IMAGE_SIZE[0])) * DNA_IMAGE_SIZE[0]
                    y1 = (i // (SIZE[1]//DNA_IMAGE_SIZE[1])) * DNA_IMAGE_SIZE[1]
                    x2 = x1 + DNA_IMAGE_SIZE[0]
                    y2 = y1 + DNA_IMAGE_SIZE[1]

                    fragmet_to_cmp = np.array(self.target_image.crop((x1,y1,x2,y2)))
                    fig = Figure((x1,y1), img=None, fragmet_to_cmp=fragmet_to_cmp)

                    self.figures.append(fig)
        
        self.score = score or sum(map(lambda f: f.score, self.figures))

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
        with MeasureTime('compose image', level='debug'):
            canvas = get_blank_image(SIZE)
            for figure in reversed(self.figures):
                canvas.alpha_composite(figure.img, figure.coordinate)
        
        return canvas
        
    def mutate(self, chance, N):
        """
        Inplace mutation of individual
        """
        if not check_chance(chance):
            return
        
        self.relevant_image = False
        with MeasureTime(f'mutation of {N} DNA', level='debug'):
            for dna in sorted(self.figures)[:N]:
                self.score -= dna.score
                dna.mutate()
                self.score += dna.score
    
    def cross(self, other):
        """
        Crossover on two individuals
        Return new instance of Individual
        """
        pivot = randint(0, len(self.figures) - 1)

        new_figures = []
        new_score = 0
        for i in range(pivot):
            fig = self.figures[i].copy()
            new_score += fig.score
            new_figures.append(fig)

        for i in range(pivot, len(other.figures)):
            fig = other.figures[i].copy()
            new_score += fig.score
            new_figures.append(fig)
        
        return Individual(self.target_image, figures=new_figures, score=new_score)

    def save(self, output_dir):
        create_dir(output_dir)
        file_name = f"genetic_{datetime.datetime.now().strftime('%d_%H_%M_%S')}.pickle"
        output_file = os.path.join(output_dir, file_name)
        with open(output_file, 'wb') as file:
            pickle.dump(self, file)
    
    @staticmethod
    def load(file_path):
        # load the last one
        if not file_path:
            file_path = sorted(get_all_files(OUTPUT_DIR))[-1]
            logging.warning(f'File is None. Load from {file_path}')

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
