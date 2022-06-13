"""Functions and classes related to stylistic choices (i.e. all
remotes should have a standard naming scheme, etc.)
"""
from _bigtree.utils import Constants


def commit_message(text: str):
    """Adds a prefix (`Constants.COMMIT_MSG_PREFIX`) to the given
    `text`.

    If no `text` is given, `Constants.COMMIT_MSG_DEFAULT` is used
    instead.
    """
    if not text:
        text = Constants.COMMIT_MSG_DEFAULT
    text = Constants.COMMIT_MSG_PREFIX + text
    return text


def name_remote(subtree_name: str) -> str:
    """For a given `subtree_name`, return the name of the remote
    according to our desired naming scheme.
    """
    return f"{subtree_name}_remote"


def is_remote_name_valid(remote_name: str) -> bool:
    """Returns `True` if `remote_name` ends in '-remote'.
    Returns `False` otherwise.
    """
    return remote_name.endswith("_remote")
