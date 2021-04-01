import random
import time

from config import numpy as np
import numpy as real_numpy
from PIL import Image

from config import (
    SIZE, EMOJI_PATH
    )
from os.path import join as join_path

from tools.image import get_image, compare_images
from tools.timer import MeasureTime
from tools import random_emoji, random_coordinate


class Figure:
    def __init__(self, coordinate, fragmet_to_cmp, img=None, score=None):
        self.coordinate = coordinate
        self.fragmet_to_cmp = fragmet_to_cmp
        self.mutate_count = 0

        if not img is None:
            self.__img = img
        else:
            self.__img = random_emoji()
        
        self.size = self.__img.size
        self.__score = score or None
        self.relevant_score = False

    @property
    def score(self):
        if not self.relevant_score:
            self.__score = compare_images(self.__img, self.fragmet_to_cmp)
            self.relevant_score = True
        return self.__score

    @property
    def img(self):
        # shitty workaround because cupy is shit
        try:
            img = Image.fromarray(self.__img.astype('uint8'))
        except AttributeError:
            img = Image.fromarray(np.asnumpy(self.__img))
        return img

    def copy(self):
        return Figure(self.coordinate, self.fragmet_to_cmp, self.__img.copy(), self.score)
    
    def mutate(self):
        self.__mutate()

    def __mutate(self):
        self.relevant_score = False
        self.mutate_count += 1
        self.__img = random_emoji()

    @property
    def compare_score(self):
        return self.score + self.mutate_count * 0.05

    def __ge__(self, value):
        return self.compare_score.__ge__(value.compare_score)
    
    def __gt__(self, value):
        return self.compare_score.__gt__(value.compare_score)
    
    def __le__(self, value):
        return value.__ge__(self)
    
    def __lt__(self, value):
        return value.__gt__(self)

    def __str__(self):
        return f"{self.__class__.__name__}{self.coordinate}"

    def __repr__(self):
        return f"{self.__class__.__name__}{self.coordinate}"
