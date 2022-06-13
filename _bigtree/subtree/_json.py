from dataclasses import dataclass
from pathlib import Path

from _bigtree.subtree import Subtree
from _bigtree.utils import Constants, JSONReader


@dataclass
class SubtreeJSONData:
    image_prefix: str
    dockercompose_files: list[str]
    tag_aliases: dict


class SubtreeJSONReader(JSONReader):
    """"""

    def __init__(self, subtree: Subtree) -> None:
        local_dir = subtree.local_directory(stringify=False)
        file = local_dir / Constants.SUBTREE_CONFIGFILE_NAME
        super().__init__(file)


class SubtreeJSON:
    bigtree_root_dir = Constants.BIGTREE_DIR

    def __init__(self, local_directory: Path) -> None:
        file = local_directory / Constants.SUBTREE_CONFIGFILE_NAME
        reader = JSONReader(file)
