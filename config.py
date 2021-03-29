import os

EMOJI_PATH = 'emoji_selected/'

DNA_IMAGE_SIZE = (16, 16)


SIZE = (512, 512)

OUTPUT_DIR = 'output'


INDIVIDUAL_SIZE = 1024

POPULATION_SIZE = 30

ITERS = 3 * 3600 * 10

GRID_DIVISION = 16

# chance of individual to mutate
MUTATION_CHACE = 0.5

# how many figues mutate 
PORTION_OF_MUTATION = 0.05


MIN_OPACTIRY = 0.3
MAX_OPACTIRY = 0.4

MIN_SCALE = 0.3
MAX_SCALE = 0.5

# rotation in degrees
MIN_ROTATION = 0
MAX_ROTATION = 0

DEFAULT_PROCESSES = 8

ON_GPU = os.environ.get('ON_GPU', False)

LOG_LEVEL = os.environ.get('LOG_LEVEL', 'warning')

TARGET_IMAGE = os.environ.get('TARGET_IMAGE', 'images/smile.jpg')

os.environ.putenv

if ON_GPU:
    print('START ON GPU'.center(35, '='))
    import cupy as numpy
else:
    import numpy