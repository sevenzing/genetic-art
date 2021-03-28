from genetic import Genetic
from tools.image import get_image
from config import SIZE
import logging
logging.basicConfig(level=logging.WARNING)

target_image = get_image('images/smile.png', SIZE)

g = Genetic(target_image)

g.run(False)
