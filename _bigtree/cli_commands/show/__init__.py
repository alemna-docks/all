import _bigtree.subtree
import _bigtree.cli_commands.show._common


def bigtree(bigtree):
    """Show all data on the `Bigtree`."""
    _bigtree.cli_commands.show._common.show_bigtree_attrs(bigtree)


def image(*subtrees):
    """For each `subtree`, print the `Subtree.name` and
    `Subtree.image_repositories`.
    """
    command = _bigtree.cli_commands.show._common.show_subtree_attributes
    if len(subtrees) == 0:
        _bigtree.subtree.cmd_for_subtrees(command)
    else:
        for subtree in subtrees:
            _bigtree.subtree.cmd_for_subtrees(command, subtree, "image_repositories")


def code(*subtrees):
    """For each `subtree`, print the `Subtree.name` and
    `Subtree.remote_repository`.
    """
    command = _bigtree.cli_commands.show._common.show_subtree_attributes
    if len(subtrees) == 0:
        _bigtree.subtree.cmd_for_subtrees(command)
    else:
        for subtree in subtrees:
            _bigtree.subtree.cmd_for_subtrees(command, subtree, "remote_repository")


def subtree(*subtrees):
    """For each `subtree`, print the `Subtree.name` and
    `Subtree.image_repositories`.
    """

    command = _bigtree.cli_commands.show._common.show_subtree_attributes
    if len(subtrees) == 0:
        _bigtree.subtree.cmd_for_subtrees(command)
    else:
        for subtree in subtrees:
            _bigtree.subtree.cmd_for_subtrees(command, subtree)
