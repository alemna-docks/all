import subprocess

import _bigtree.cli_commands.image._build
import _bigtree.cli_commands.image._push
import _bigtree.subtree


def build(*subtrees):
    """For each `subtree`, go to the `subtree.local_directory`
    and run `docker compose up --build`.
    """

    def _build(_subtree_name_pattern=None):
        """An internal function executing the
        `docker compose up --build` command.
        """
        raise NotImplementedError

    if len(subtrees) == 0:
        _build()
    else:
        for subtree in subtrees:
            _build(subtree)


def push(*subtrees):
    """For each tag in each `subtree`, go to the
    `subtree.local_directory` and run `docker push -t <tag>`.
    """

    def _push(_subtree_name_pattern=None):
        """An internal function executing the `docker push`
        command.
        """
        if _subtree_name_pattern is None:
            factory = _bigtree.subtree.create_subtree_factory()
        else:
            s = _subtree_name_pattern
            factory = _bigtree.subtree.create_subtree_factory(subtree_name_pattern=s)

        for subtree in factory:
            cmds = [f"cd {subtree.local_directory}", ()]
            raise NotImplementedError
            sp = subprocess.call(" && ".join(cmds), shell="/bin/bash")

    if len(subtrees) == 0:
        _push()
    else:
        for subtree in subtrees:
            _push(subtree)
