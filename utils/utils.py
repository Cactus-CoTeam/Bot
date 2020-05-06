import logging


def get_logger():
    logger = logging.getLogger()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
    return logger