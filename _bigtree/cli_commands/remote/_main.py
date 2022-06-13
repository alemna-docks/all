__all__ = ["add", "fetch", "merge"]
import _bigtree.bigtree
import _bigtree.subtree
import _bigtree.utils.style
from _bigtree.bigtree import Bigtree
from _bigtree.subtree import Subtree


def add(new_remote_name: str):
    if new_remote_name.endswith("_remote"):
        new_subtree_name = new_remote_name.removesuffix("_remote")
    else:
        new_subtree_name = new_remote_name
        new_remote_name = _bigtree.utils.style.name_remote(new_remote_name)

    try:
        subtree = Subtree(new_subtree_name)
    except KeyError as ke:
        print(
            f"Cannot add remote! No subtree named {new_subtree_name} has been "
            + "configured."
        )
    if subtree.disable_subtree is True:
        pass
    else:
        Bigtree().add_remote(
            remote_name=new_remote_name,
            remote_url=subtree.remote_repository,
            prefix=subtree.local_directory(),
        )


def fetch(subtree_name_patterns: list):
    for pattern in subtree_name_patterns:
        subtrees = [s for s in _bigtree.subtree.create_subtree_factory(pattern)]
        for subtree in subtrees:
            if subtree.disable_subtree is True:
                print(f"Subtree '{subtree.name}' is disabled, skipping...")
            else:
                remote_name = _bigtree.utils.style.name_remote(subtree.name)
                try:
                    f = Bigtree().remote(name=remote_name).fetch()
                except KeyError:
                    m = f"Adding remote '{remote_name}' at {subtree.remote_repository}"
                    print(m)
                    Bigtree().add_remote(
                        remote_name=remote_name,
                        remote_url=subtree.remote_repository,
                        prefix=subtree.local_directory(absolute=False, stringify=True),
                    )
                    f = Bigtree().remote(name=remote_name).fetch()

                for info in f:
                    print(f"Latest commit at {remote_name}: {info.commit}")


def merge(subtree_name_patterns: list):
    for pattern in subtree_name_patterns:
        remote_name = _bigtree.utils.style.name_remote(pattern)
        r = Bigtree().remote(name=remote_name)
        commits_ahead = _bigtree.bigtree.remote_commits_ahead(r)
        print(f"{remote_name} is {commits_ahead} commits ahead of local 'main'.")
        if commits_ahead > 0:
            subtrees = [s for s in _bigtree.subtree.create_subtree_factory(pattern)]
            for s in subtrees:
                Bigtree().pull_remote(subtree=s, remote=r)
