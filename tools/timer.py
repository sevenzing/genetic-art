import timeit
import logging

class MeasureTime:
    def __init__(self, name=None, level='info'):
        self.level = level
        self.name = f" '{name}'" if name else ''

    def __enter__(self):
        self.start = timeit.default_timer()

    def __exit__(self, exc_type, exc_value, traceback):
        self.took = (timeit.default_timer() - self.start) * 1000.0
        msg = f"Code block{self.name} took: {self.took} ms"
        
        if self.level == 'info':
            logging.info(msg)
        else:
            logging.debug(msg)
