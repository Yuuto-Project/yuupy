import dotenv
import logging
import os

if os.path.exists('.env'):
    dotenv.load_dotenv('.env')

# Get logging level. If not defined, use 20 (INFO)
log_level = os.getenv('LOGGING_LEVEL') or 20
LEVEL = int(log_level)

# Set up the logger
logger = logging.getLogger()
logger.setLevel(LEVEL)

# Console Handler
ch = logging.StreamHandler()
ch.setLevel(LEVEL)

# Format for Logging
# [LEVEL] YYYY/MM/DD hh:mm:ss @ MODULE - MESSAGE
LOG_FORMAT = '[%(levelname)s] %(asctime)s @ %(module)s - %(message)s'
DATE_FORMAT = '%Y/%m/%d %H:%M:%S'
formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

ch.setFormatter(formatter)

logger.addHandler(ch)

# File handler
if os.getenv('LOG_FILE') == 'True':
    fh = logging.FileHandler('yuuto.log', "w", encoding="UTF-8")
    fh.setLevel(LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logging.info('Logging to file started')
