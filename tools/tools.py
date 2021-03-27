import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool, cpu_count
from config import (
    MIN_OPACTIRY, MAX_OPACTIRY,
    MIN_ROTATION, MAX_ROTATION,
    MIN_SCALE, MAX_SCALE,
)

def check_chance(chance):
    return random.random() <= chance


def parallelize_task(target, args_list, max_workers=8):
    """
    Parallelize function call using threads
    """
    if isinstance(args_list, int):
        args_list = [() for _ in range(args_list)]

    with ThreadPoolExecutor(max_workers) as executor:
        futures = [executor.submit(target, *args) for args in args_list]
        result = [future.result() for future in as_completed(futures)]
    return result


def multiprocess_task(target, arg_list, max_workers=cpu_count()):
    """
    
    """
    with Pool(max_workers) as pool:
        return pool.map(
            target,
            arg_list,
        )


def random_opacity():
    return random.uniform(MIN_OPACTIRY, MAX_OPACTIRY)

def random_scale():
    return random.uniform(MIN_SCALE, MAX_SCALE)

def random_rotation():
    return random.randint(MIN_ROTATION, MAX_ROTATION)
