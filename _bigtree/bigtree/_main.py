from dataclasses import dataclass

import _bigtree.utils.style
from _bigtree.bigtree._git import BigtreeGit
from _bigtree.subtree import Subtree
from _bigtree.utils import Constants


@dataclass(frozen=True)
class BigtreeData:
    """"""

    subtrees: set[Subtree]
    subtree_dict: dict
    subtree_names: set[str]


class Bigtree(BigtreeGit):
    """"""

    # TODO: Make a base class so we don't have this duplicated
    root_dir = Constants.BIGTREE_DIR

    def __init__(self) -> None:
        super().__init__()

        subtrees = set()
        subtree_dict = {}
        subtree_names = set()
        for child in self.root_dir.iterdir():
            if (
                child.is_dir()
                and child.name.startswith(".") is False
                and child.name.startswith("_") is False
            ):
                try:
                    subtree = Subtree(name=child.name)
                    subtree_dict[child.name] = subtree
                    subtree_names.add(child.name)
                    subtrees.add(subtree)
                except KeyError:
                    print("foo bar")

        self._data = BigtreeData(
            subtrees=subtrees,
            subtree_dict=subtree_dict,
            subtree_names=subtree_names,
        )

    @property
    def data(self):
        return self._data

    @property
    def subtree_dict(self):
        return self._data.subtree_dict

    @property
    def subtree_names(self):
        return self._data.subtree_names

    @property
    def subtrees(self):
        return self._data.subtrees

    def subtree(self, subtree_name):
        return self._data.subtree_dict[subtree_name]

    def add_subtree(self, subtree: Subtree):
        remote_name = _bigtree.utils.style.name_remote(subtree_name=subtree.name)
        return self.add_remote(
            remote_name=remote_name,
            remote_url=subtree.remote_repository,
            prefix=subtree.local_directory(absolute=False, stringify=False),
        )

    def delete_subtree(self, subtree: Subtree):
        remote_name = _bigtree.utils.style.name_remote(subtree_name=subtree.name)
        return self.delete_remote(remote=remote_name)
