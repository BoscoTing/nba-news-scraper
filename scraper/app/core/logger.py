import os
import logging
import sys

from logging.handlers import RotatingFileHandler


logger = logging.getLogger('scraper')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(filename)s | %(module)s.%(funcName)s: ' +
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

os.makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/scraper.log',
                                   maxBytes=10485760,  # 10MB
                                   backupCount=5)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
    logger.critical('Critical message')
