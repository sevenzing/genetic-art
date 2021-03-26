from figures import get_random_figure
from config import INDIVIDUAL_SIZE
from tools.timer import MeasureTime
from tools.image import compare_images, Image, get_blank_image
from tools import check_chance

from config import SIZE


class Individual:
    def __init__(self, figures=None):
        self.score = 0
        self.relevant_image = False
        self.__img = None


        with MeasureTime('creating one gen'):
            self.data = figures or [
                get_random_figure()
                for _ in range(INDIVIDUAL_SIZE)
            ]
    
    def fitness(self) -> float:
        """
        Return fitness value of individual
        """

    @property
    def img(self):
        if not self.relevant_image:
            self.__img = self._get_full_image()
            self.relevant_image = True
        
        return self.__img

    def _get_full_image(self) -> Image.Image:
        """
        Return composed image of individual
        """
        canvas = get_blank_image(SIZE)
        for dna in self.data:
            canvas.alpha_composite(dna.img)
        
        return canvas
        
    def mutate(self, chance):
        """
        Inplace mutation of individual
        """
        if not check_chance(chance):
            return
        
        self.relevant_image = False
        with MeasureTime('mutation'):
            for dna in self.data:
                dna.mutate()
        