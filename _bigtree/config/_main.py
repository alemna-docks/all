from dataclasses import dataclass
from types import MappingProxyType
from typing import Union

from _bigtree.utils import Constants, JSONReader


class ConfigJSONReader(JSONReader):
    """A `JSONReader` which will automatically read the config file
    named by `_bigtree.utils.Constants.CONFIGFILE_PATH`.
    """

    def __init__(self) -> None:
        super().__init__(file=Constants.CONFIGFILE_PATH)


class BigtreeReader(ConfigJSONReader):
    def __init__(self) -> None:
        super().__init__()
        self._data = Config.bigtree


class SubtreeReader(ConfigJSONReader):
    def __init__(self, subtree_name: Union[str, None] = None) -> None:
        super().__init__()
        self._data = Config.subtrees
        if subtree_name is not None:
            self._data = Config.subtrees[subtree_name]


@dataclass(frozen=True)
class Config:
    """"""

    # Dataclasses can't have mutable default values. So, we
    # use MappingProxyType as basically a 'frozen' dict.
    full_config = MappingProxyType(ConfigJSONReader().data)

    bigtree = MappingProxyType(full_config["bigtree"])
    subtrees = MappingProxyType(full_config["subtrees"])
    base_images = tuple(full_config["base_images"])
