from genetic import Genetic
from tools.image import get_image
import logging


logging.basicConfig(level=logging.INFO)

target_image = get_image('images/she.jpg')

g = Genetic(target_image)