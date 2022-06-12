from pathlib import Path
from typing import Any


def debug_msg(*messages):
    first_message = messages[0]
    print(f"(DEBUG) {first_message}")
    if len(messages) > 1:
        for message in messages[1:]:
            print(f"(DEBUG)   {message}")


def get_bigtree_root() -> Path:
    """Returns the absolute path to the directory containing the
    indicator file. It searches this file's directory and then
    moves upwards through all parent directories. If no indicator
    file is found, it raises `FileNotFoundError`.
    """
    this_file = Path(__file__)
    parent_directories = this_file.parents
    indicator_file_name = "bigtree"

    # Search
    for dir in parent_directories:
        indicator_file_path = dir / indicator_file_name
        if indicator_file_path.exists() and indicator_file_path.is_file():
            return dir.resolve()

    # If we searched and didn't find anything
    raise FileNotFoundError(
        'Could not find the "bigtree root indicator" file,' + f" {indicator_file_name}."
    )


def get_attrs(object: Any, include_internal: bool = False) -> dict:
    """For a given object, return a list of properties."""
    # properties: dict = object.__dict__
    attr_list: list = dir(object)
    attrs = {}

    for attribute in attr_list:
        if attribute.startswith("__") and attribute.endswith("__"):
            # always skip builtins
            pass
        else:
            attrs[attribute] = getattr(object, attribute)

    if include_internal is False:
        keys_to_remove = set()
        for key in attrs.keys():
            key_name = str(key)
            if key_name.startswith("_"):
                keys_to_remove.add(key)
        for key in keys_to_remove:
            attrs.pop(key)

    return attrs
