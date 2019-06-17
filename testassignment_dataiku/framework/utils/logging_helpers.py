import logging


def set_log():
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(format='%(message)s')
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    return log
