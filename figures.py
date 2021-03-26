import random
from config import SIZE, MIN_OPACTIRY, MIN_SCALE
from tools.image import get_blank_image, get_image, apply_matrix, set_opacity_inplace
from tools.timer import MeasureTime
import numpy as np
import time



class Figure:
    source = None
    def __init__(self, x=None, y=None, rotation=None, opacity=None, scale=None):
        self.x = x or random.randint(0, SIZE[0])
        self.y = y or random.randint(0, SIZE[1])
        self.rotation = rotation or random.randint(0, 360)
        self.opacity = opacity or random.uniform(MIN_OPACTIRY, 1)
        self.scale = scale or random.uniform(MIN_SCALE, 1)
        self.source = self.__class__.source

        self.update()

    def copy(self):
        return self.__class__(self.x, self.y, self.rotation, self.opacity, self.scale)

    def update(self):
        self.img = self.__get_image()
    
    def mutate(self, n=1):
        for mode in random.sample(range(5), n):
            self.__mutate(mode)
        self.update()

    def __mutate(self, mode):
        assert 0 <= mode <= 4
        if mode == 0:
            self.x = random.randint(0, SIZE[0])
        elif mode == 1:
            self.y = random.randint(0, SIZE[1])
        elif mode == 2:
            self.rotation = random.randint(0, 360)
        elif mode == 3:
            self.opacity = random.uniform(MIN_OPACTIRY, 1)
        elif mode == 4:
            self.scale = random.uniform(MIN_SCALE, 1)


    def __get_image(self):
        """
        Return image
        """
        img = self.source.copy()
        set_opacity_inplace(img, self.opacity)
        return apply_matrix(img, self.x, self.y, self.rotation, self.scale)

    def __str__(self):
        return f"{self.__class__.__name__}{self.x, self.y, self.rotation, self.opacity, self.scale}"

    def __repr__(self):
        return f"{self.__class__.__name__}{self.x, self.y}"

class Cat(Figure):
    source = get_image('images/cat.jpg')




def get_random_figure() -> Figure:
    return random.choice(FIGURES)()


FIGURES = [
    Cat,
]
