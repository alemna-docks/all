import sys

from _bigtree.cli_parser import (
    IncompatibleArgumentError,
    execute_parser,
    initialize_parser,
)
from _bigtree.log import initialize_logger

logger = initialize_logger()
parser = initialize_parser()
try:
    execute_parser(parser, args=sys.argv[1:])
except IncompatibleArgumentError as iae:
    print(f"ERROR: {iae.message}")
