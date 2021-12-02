from os import path, remove
import logging.config

if path.isfile("../python_logging.log"):
    remove("../python_logging.log")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logger_handler = logging.FileHandler("../python_logging.log")
logger_handler.setLevel(logging.DEBUG)

logger_formatter = logging.Formatter('%(asctime)s  %(levelname)-8s %(message)s (%(filename)s:%(lineno)d)')
logger_handler.setFormatter(logger_formatter)

logger.addHandler(logger_handler)


