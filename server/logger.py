import logging

def setup_logging(name):
    # create logger object
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to console handler
    ch.setFormatter(formatter)

    # add console handler to logger
    logger.addHandler(ch)
    
    return logger