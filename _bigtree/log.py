import logging
import sys
from logging import CRITICAL, DEBUG, ERROR, INFO, WARN, WARNING, Logger, StreamHandler


def initialize_logger() -> Logger:
    _l = logging.getLogger()
    _l.addHandler(StreamHandler())
    return _l
