import random
import time

import numpy as np

from config import (
    SIZE,
    )
from tools.image import (apply_matrix, get_image,
                         set_opacity_inplace)
from tools.timer import MeasureTime
from tools import random_opacity, random_rotation, random_scale


class Figure:
    source = None
    def __init__(self, x=None, y=None, rotation=None, opacity=None, scale=None, img=None):
        self.x = x or random.randint(0, SIZE[0])
        self.y = y or random.randint(0, SIZE[1])
        self.rotation = rotation or random_rotation()
        self.opacity = opacity or random_opacity()
        self.scale = scale or random_scale()
        
        self.source = self.__class__.source
        if img:
            self.img = img
        else:
            self.img = self.__get_image()

    def copy(self):
        return self.__class__(self.x, self.y, self.rotation, self.opacity, self.scale, self.img.copy())

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
            self.rotation = random_rotation()
        elif mode == 3:
            self.opacity = random_opacity()
        elif mode == 4:
            self.scale = random_scale()


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
    source = get_image('images/cat.jpg', (512, 512))

class Cat2(Figure):
    source = get_image('images/cat2.jpg', (512, 256))



def get_random_figure() -> Figure:
    return random.choice(FIGURES)()


FIGURES = [
    Cat,
    Cat2,
]
