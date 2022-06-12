import logging
from logging import Logger, StreamHandler
from logging import DEBUG, INFO, WARN, WARNING, ERROR, CRITICAL
import sys


def initialize_logger() -> Logger:
    _l = logging.getLogger()
    _l.addHandler(StreamHandler())
    return _l
