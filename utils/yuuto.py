import logging


LEVEL = logging.INFO

# Set up the logger
logger = logging.getLogger()
logger.setLevel(LEVEL)

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(LEVEL)

# Format for Logging
# [LEVEL] YYYY/MM/DD HH:mm:SS @ MODULE - MESSAGE
LOG_FORMAT = '[%(levelname)s] %(asctime)s @ %(module)s - %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

ch.setFormatter(formatter)

logger.addHandler(ch)