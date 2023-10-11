import logging

def create_logger(name: str, level: int, formatter=None):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    if formatter is None:
        formatter = logging.Formatter('%(asctime)s %(filename)s - %(funcName)s [%(levelname)-s] - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger