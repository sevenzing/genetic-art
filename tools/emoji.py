from config import EMOJI_PATH, DNA_IMAGE_SIZE
from .image import get_raw_image
from .tools import get_all_files
from .timer import MeasureTime
import random


ALL_EMOJI_NAMES = get_all_files(EMOJI_PATH)


ALL_EMOJI = list(map(lambda path: get_raw_image(path, DNA_IMAGE_SIZE), ALL_EMOJI_NAMES))

def random_emoji():
    return random.choice(ALL_EMOJI)
