import os
import sys
import logging

# Python Logging
environment = os.environ.get("PROJECT_ENV")
if environment == "production" or environment == "staging":
    logging.basicConfig(format="%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s",
                        filename="app.log",
                        filemode="a",
                        level=logging.INFO)
else:
    logging.basicConfig(format="%(asctime)s - %(name)s - "
                               "%(levelname)s - %(message)s",
                        level=logging.DEBUG)

logger = logging.getLogger(__name__)


class Logger:
    @staticmethod
    def debug(message, *args):
        logger.debug(message, *args)

    @staticmethod
    def info(message, *args):
        logger.info(message, *args)

    @staticmethod
    def warning(message, *args):
        logger.warning(message, *args)

    @staticmethod
    def exception(message, *args):
        logger.exception(message, *args)

    @staticmethod
    def error(message, *args):
        logger.error(message, *args)

    @staticmethod
    def critical(message, *args):
        logger.critical(message, *args)

        sys.exit("CRITICAL ERROR. EXITING PROGRAM.")
