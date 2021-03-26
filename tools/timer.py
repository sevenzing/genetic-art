import timeit
import logging

class MeasureTime:
    def __init__(self, name=None):
        self.name = f" '{name}'" if name else ''

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        logging.info(f"Code block{self.name} took: {self.took} ms")
