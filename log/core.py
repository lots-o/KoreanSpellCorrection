import os
import logging
from logging.handlers import TimedRotatingFileHandler


import autologging
from colorama import Fore, Style

ROOT_LOGGER_NAME = "KoreanSpellCorrection"
FORMAT = "%(levelname)s::%(asctime)s::%(filename)s-%(lineno)d::%(name)s::%(funcName)s::%(message)s"
_logger = None


class ColorFormatter(logging.Formatter):
    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            autologging.TRACE: Fore.LIGHTBLUE_EX + self.fmt + Fore.RESET,
            logging.DEBUG: Fore.GREEN + self.fmt + Fore.RESET,
            logging.INFO: Fore.BLUE + self.fmt + Fore.RESET,
            logging.WARNING: Fore.YELLOW + self.fmt + Fore.RESET,
            logging.ERROR: Fore.RED + Style.BRIGHT + self.fmt + Fore.RESET + Style.RESET_ALL,
            logging.CRITICAL: Fore.RED + self.fmt + Fore.RESET,
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def getLogger(name="", log_level=None):

    if name:
        logger = logging.getLogger(ROOT_LOGGER_NAME + "." + name)
    else:
        logger = logging.getLogger(ROOT_LOGGER_NAME)

    if log_level:
        logger.setLevel(log_level)
    return logger


def logged(obj):
    if isinstance(obj, logging.Logger):
        return autologging.logged(obj)  # `@logged(_logger)'
    else:
        return autologging.logged(getLogger())(obj)  # `@logged`


def traced(obj, *args):
    if isinstance(obj, logging.Logger):  # `@traced(_logger)'
        return autologging.traced(obj, *args)
    elif isinstance(obj, str):  # `@traced('method')'
        return autologging.traced(getLogger(), obj, *args)
    else:  # `@traced'
        return autologging.traced(getLogger(), *args)(obj)


def setup_logger(
    logger: logging.Logger,
    formatter: logging.Formatter = None,
    log_level=autologging.TRACE,
) -> None:

    # stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # file handler
    # FILE HANDLER => export LOG_PATH = TARGET_FILE_PATH
    log_path = os.getenv("LOG_PATH", "")
    if log_path:
        file_handler = TimedRotatingFileHandler(filename=log_path, when="midnight", interval=1, encoding="utf-8")
        file_handler.suffix = "-%Y%m%d"
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False

    if logger.level == logging.NOTSET:
        logger.setLevel(log_level)


_logger = setup_logger(getLogger(), ColorFormatter(FORMAT))
