from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from types import FunctionType

from _bigtree.config import SubtreeReader
from _bigtree.utils import Constants


@dataclass
class SubtreeData:
    """A dataclass to hold data read from the `subtrees.json` file."""

    local_directory: Path
    """A local directory to store the subtree in."""
    remote_repository: str
    """A remote Git repository to pull from and push to."""
    remote_branch: str
    """Branch on `remote_repository` to track."""
    image_repositories: list[str]
    """Docker image repositories (like Docker Hub) to push images to."""
    disable_subtree: bool
    """If True, instructs the program that this Subtree exists in `config.json` only."""


class Subtree:

    bigtree_root: Path = Constants.BIGTREE_DIR

    def __init__(self, name) -> None:
        self._name = name
        reader = SubtreeReader(subtree_name=self._name)
        self._data = SubtreeData(
            local_directory=self.bigtree_root / reader.get("local_directory"),
            remote_repository=reader.get("remote_repository"),
            remote_branch=reader.get_optional("remote_branch")
            if reader.get_optional("remote_branch") is not None
            else Constants.DEFAULT_BRANCH,
            image_repositories=reader.get("image_repositories"),
            disable_subtree=reader.get_optional("disable_subtree")
            if reader.get_optional("disable_subtree") is not None
            else False,
        )

    @property
    def name(self) -> str:
        return self._name

    def local_directory(self, absolute=True, stringify=True) -> str | Path:
        """The directory the subtree 'lives' in. By default `local_directory` is
        returned as an absolute path in string form, but this can be modified by
        setting `absolute` or `stringify` as False.

        When `absolute` is False, the relative path is given relative to the
        bigtree root directory.
        """
        if not absolute and not stringify:
            return self._data.local_directory.relative_to(self.bigtree_root)
        elif absolute is True and not stringify:
            return self._data.local_directory.resolve()
        elif stringify is True and not absolute:
            return str(self._data.local_directory.relative_to(self.bigtree_root))
        else:  # stringify and absolute
            return str(self._data.local_directory.resolve())

    @property
    def remote_branch(self) -> str:
        """The branch being tracked on the `remote_repository`."""
        return self._data.remote_branch

    @property
    def remote_repository(self) -> str:
        """The URL of a remote Git repository whose `main` branch will be
        tracked by this subtree.
        """
        return self._data.remote_repository

    @property
    def image_repositories(self) -> list[str]:
        """A list containing the URLs to one or more Docker image
        repositories.
        """
        return self._data.image_repositories

    @property
    def disable_subtree(self) -> bool:
        """A boolean value. If `True`, skip this subtree."""
        return self._data.disable_subtree


def create_subtree_factory(subtree_name_pattern: str = None):
    """A Generator that returns any subtrees that match the
    given regex `subtree_name_pattern`. If `subtree_name_pattern`
    is None, it will yield all valid subtrees.
    """
    # print(f"PATTERN: {subtree_name_pattern}")
    if subtree_name_pattern is None:
        # '.+' is 'one or more of any character'
        subtree_name_pattern = ".+"

    reader = SubtreeReader(subtree_name=None)
    subtree_data: dict = reader.data
    # print(f"ALL KEYS: {subtree_data.keys()}")
    for key in subtree_data.keys():
        # print(f"Searching {key}")
        if re.search(subtree_name_pattern, key):
            yield Subtree(name=key)
        else:
            pass


def cmd_for_subtrees(
    command: FunctionType, subtree_name_patterns: list[str], *cmd_args
):
    # TODO: Rewrite documentation
    """Runs one or more `commands()` against every Subtree matching the
    `subtree_name_pattern`. If no `subtree_name_pattern` is given,
    matches all Subtrees.
    """
    for pattern in subtree_name_patterns:
        factory = create_subtree_factory(subtree_name_pattern=pattern)

        for subtree in factory:
            if cmd_args:
                command(subtree, *cmd_args)
            else:
                command(subtree)
