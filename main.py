from genetic import Genetic
from tools.image import get_image
from config import SIZE, TARGET_IMAGE, LOG_LEVEL
import logging


level = logging.getLevelName(LOG_LEVEL.upper())

print(f"Set log level to {level}")

logging.basicConfig(level=level)

target_image = get_image(TARGET_IMAGE, SIZE)

g = Genetic(target_image)

g.run(False)
