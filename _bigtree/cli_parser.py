from argparse import ArgumentParser

import _bigtree.cli_commands.image
import _bigtree.cli_commands.remote
import _bigtree.cli_commands.show
import _bigtree.log
import _bigtree.utils
from _bigtree.exceptions import IncompatibleArgumentError
from _bigtree.bigtree import Bigtree

logger = _bigtree.log.initialize_logger()


def initialize_parser() -> ArgumentParser:
    _d = (
        "Run pre-defined workflows on any subtrees "
        + "matching a regular-expression SUBTREE_NAME_PATTERN."
    )
    _e = (
        "Additional help for SUBCOMMANDS can be accessed by typing "
        + "`--help` after that subcommand's name (for example, "
        + "`bigtree remote --help`). In general, the `--help` "
        + "command overrides other commands (even `--verbose`)."
    )
    parser = ArgumentParser(prog="bigtree", description=_d, epilog=_e)

    #
    # One or more SUBTREE_NAME_PATTERNs
    #
    subtree_name_help = (
        "One or more regular-expression patterns. The desired "
        + "commands will be executed on subtrees whose names "
        + "match the pattern(s). Leave blank to include all "
        + "subtrees when carrying out commands."
    )
    parser.add_argument(
        "subtree_name_pattern",
        action="store",
        nargs="*",
        # If no name pattern is given, default name pattern will match all
        default=[".+"],
        help=subtree_name_help,
        metavar="SUBTREE_NAME_PATTERN",
    )
    #
    # --debug, --verbose, -v
    #
    debug_help = "explain what the program is doing while it executes commands"
    parser.add_argument(
        "--debug",
        "--verbose",
        "-v",
        action="store_true",
        help=debug_help,
        dest="verbose",
    )
    #
    # --all, --include-disabled
    #
    all_help = (
        "include subtrees whose names match the pattern(s) given, "
        + "even if they have `disable_subtree: true` in subtrees.json"
    )
    parser.add_argument(
        "--all",
        "--include-disabled",
        action="store_true",
        help=all_help,
        dest="include_disabled",
    )
    #
    # Yay, subcommands!
    #
    sp_help = "subcommands giving access to workflows, like `remote --fetch` and `image --push`"
    sp = parser.add_subparsers(title="SUBCOMMANDS", help=sp_help)

    # bigtree remote ...
    #   ... --add
    #   ... --fetch
    #   ... --merge
    #   ... --show
    remote = sp.add_parser("remote")
    remote.add_argument("--add")
    remote.add_argument("--fetch", action="store_true")
    remote.add_argument("--merge", action="store_true")
    remote.add_argument("--show", action="store_true")

    # bigtree image ...
    #   ... --build
    #   ... --push
    #   ... --show
    image = sp.add_parser("image")
    image.add_argument("--build", action="store_true")
    image.add_argument("--push", action="store_true")
    image.add_argument("--show", action="store_true")

    # bigtree show ...
    #   ... --bigtree
    #   ... --subtree
    #   ... --remote
    #   ... --image
    show = sp.add_parser("show")
    show.add_argument("--bigtree", action="store_true")
    show.add_argument("--subtree", action="store_true")
    show.add_argument("--remote", action="store_true")
    show.add_argument("--image", action="store_true")

    return parser


def execute_parser(parser: ArgumentParser, args):
    debug = _bigtree.utils.debug_msg
    parsed = parser.parse_args(args)
    if parsed.verbose:
        logger.setLevel(_bigtree.log.DEBUG)
        logger.debug("debug level set")
        debug("Debug mode enabled.")
        debug("Arguments recieved from command-line:", args)
        debug("Arguments parsed from command-line:", parsed)

    if "remote" in args:
        if parsed.include_disabled and any((parsed.fetch, parsed.merge)):
            raise IncompatibleArgumentError("--include-disabled", "--fetch", "--merge")

        if parsed.add:
            _bigtree.cli_commands.remote.add(parsed.add)
        if parsed.fetch:
            _bigtree.cli_commands.remote.fetch(parsed.subtree_name_pattern)
        if parsed.merge:
            _bigtree.cli_commands.remote.merge(parsed.subtree_name_pattern)
        if parsed.show:
            _bigtree.cli_commands.show.remote(parsed.subtree_name_pattern)

    elif "image" in args:
        if parsed.build:
            _bigtree.cli_commands.image.build(parsed.subtree_name_pattern)
        if parsed.push:
            _bigtree.cli_commands.image.push(parsed.subtree_name_pattern)
        if parsed.show:
            _bigtree.cli_commands.show.image(parsed.subtree_name_pattern)

    elif "show" in args:
        if parsed.bigtree:
            _bigtree.cli_commands.show.bigtree(Bigtree())
        if parsed.subtree:
            # Even if other flags like --image and --remote are present,
            # show.subtree() will cover all the same data anyways. Call
            # it and exit.
            _bigtree.cli_commands.show.subtree(parsed.subtree_name_pattern)
        else:
            if parsed.image:
                _bigtree.cli_commands.show.image(parsed.subtree_name_pattern)
            if parsed.remote:
                _bigtree.cli_commands.show.remote(parsed.subtree_name_pattern)

    else:  # arguments don't match any command
        parser.print_help()


if __name__ == "__main__":
    pass
