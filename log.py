import logging
from logging import handlers
import sys

_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger('')
logger.setLevel(logging.DEBUG)

_streamHandler = logging.StreamHandler(sys.stdout)
_streamHandler.setLevel(logging.DEBUG)
_streamHandlerFormatter = logging.Formatter(fmt="%(asctime)s (%(levelname)s): %(message)s", datefmt=_DATE_FORMAT)
_streamHandler.setFormatter(_streamHandlerFormatter)
logger.addHandler(_streamHandler)

_fileHandler = logging.handlers.RotatingFileHandler(filename='foodorder-slackbot.log', maxBytes=(50 * 100000), backupCount=3)
_fileHandler.setLevel(logging.WARNING)
_fileHandlerFormatter = logging.Formatter(fmt="%(asctime)s (%(levelname)s): %(message)s", datefmt=_DATE_FORMAT)
_fileHandler.setFormatter(_fileHandlerFormatter)
logger.addHandler(_fileHandler)
