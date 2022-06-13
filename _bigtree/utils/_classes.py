import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Union

from _bigtree.utils._functions import get_bigtree_root


@dataclass(frozen=True)
class Constants:
    BIGTREE_DIR: Path = get_bigtree_root()
    """The root directory for the bigtree, given as an absolute `Path` object."""
    BIGTREE_APP_DIR: Path = BIGTREE_DIR / "_bigtree"
    """The application directory for the bigtree, given as an absolute `Path` object."""

    CONFIGFILE_NAME: str = "config.json"
    """The name of bigtree's config file, given as string name plus extension."""
    CONFIGFILE_PATH: Path = BIGTREE_APP_DIR / CONFIGFILE_NAME
    """The absolute path of bigtree's config file."""

    COMMIT_MSG_PREFIX: str = "(🥦 bigtree) "
    """Append this string to the beginning of any commit messages made by bigtree"""
    COMMIT_MSG_DEFAULT: str = "no message specified"
    "A message to be used as a commit message when no message is otherwise provided."

    DEFAULT_BRANCH: str = "main"
    """Default branch to use for any Git repository without a default
    branch specified in the bigtree config file (usually `settings.json`)."""

    SUBTREE_CONFIGFILE_NAME: str = "bigtree.subtree.json"
    """The name of a config file which will be at the root of each subtree."""


class JSONReader:
    """Opens the specified JSON file and returns values.

    If `file` is given as a relative `Path`, then `JSONReader` will
    interpret it relative to `_bigtree.utils.Constants.BIGTREE_DIR`.
    """

    def __init__(self, file: Union[str, Path]) -> None:
        if isinstance(file, Path):
            if file.is_absolute:
                file = str(file)
            else:  # filepath is relative
                file = Constants.BIGTREE_DIR / file
                file = str(file)
        with open(file=file, mode="r") as file:
            # JSON comments technically aren't in the JSON spec, and so
            # they aren't supported by Python's built-in JSON parser. So,
            # we make sure to strip lines starting with '//'.
            file_contents = "".join(
                line for line in file if not line.strip().startswith("//")
            )
            file_as_json = json.loads(file_contents)
            self._data: dict = file_as_json

    @property
    def data(self) -> dict:
        """A dict holding the file's JSON data as a `dict`."""
        return self._data

    def pretty_data(self, indent: Union[int, str, None] = 2) -> str:
        """The file's JSON data, turned into a string and pretty-ified
        with proper indentation.
        """
        return json.dumps(self.data, indent=indent)

    def get(self, key: str) -> Any:
        """Returns whatever value is associated with the given `key`
        in this Reader's `.data`. If no such key exists, Python will
        raise a `KeyError`.

        To return `None` instead of raising `KeyError`, use
        `JSONReader.get_optional()`.
        """
        return self.data[key]

    def get_optional(self, key: str) -> Any:
        """A method to access a JSON field that may or may not exist.
        If it doesn't exist, this method returns `None` instead of
        raising `KeyError`.
        """
        try:
            return self.get(key)
        except KeyError:
            return None
