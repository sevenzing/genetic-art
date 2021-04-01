import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count
from config import (
    GRID_DIVISION, SIZE,
    DEFAULT_PROCESSES,
    ON_GPU,
)
from os import listdir, makedirs
from os.path import isfile, join


def check_chance(chance):
    return random.random() <= chance


def parallelize_task(target, args_list, max_workers=DEFAULT_PROCESSES):
    """
    Parallelize function call using threads
    """
    if isinstance(args_list, int):
        args_list = [() for _ in range(args_list)]
    
    if ON_GPU:
        # No threads
        result = [target(*args) for args in args_list]
    else:
        with ThreadPoolExecutor(max_workers) as executor:
            futures = [executor.submit(target, *args) for args in args_list]
            result = [future.result() for future in as_completed(futures)]
    
    return result


def random_coordinate():
    x = round(random.randint(0, SIZE[0]) / GRID_DIVISION) * GRID_DIVISION
    y = round(random.randint(0, SIZE[1]) / GRID_DIVISION) * GRID_DIVISION
    return x, y
    


def get_all_files(directory):
    return [
        join(directory, f) 
            for f in listdir(directory) 
                if isfile(join(directory, f)) and not f.startswith('.')
        ]

def create_dir(path):
    try:
        makedirs(path)
    except FileExistsError:
        pass