import sys
import logging
import logging.handlers

_logger = None


def logger():
    global _logger
    if not _logger:
        _logger = logging.getLogger(__name__)
        _logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s (%(levelname)s): %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'))
        _logger.addHandler(stream_handler)

        file_handler = logging.handlers.RotatingFileHandler(
            filename='foodorder-slackbot.log', maxBytes=(50 * 100000), backupCount=3)
        file_handler.setLevel(logging.WARNING)
        file_handler.setFormatter(
            logging.Formatter(
                fmt="%(asctime)s (%(levelname)s): %(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'))
        _logger.addHandler(file_handler)

    return _logger
