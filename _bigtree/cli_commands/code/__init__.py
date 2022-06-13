from _bigtree.cli_commands.code._main import *

# import _bigtree.bigtree
# import _bigtree.subtree
# import _bigtree.utils.style
# from _bigtree.bigtree import Bigtree


# def fetch(subtree_name_patterns: list):
#     for pattern in subtree_name_patterns:
#         remote_name = _bigtree.utils.style.name_remote(pattern)
#         f = Bigtree().remote(name=remote_name).fetch()
#         for info in f:
#             print(f"Latest commit at {remote_name}: {info.commit}")


# def merge(subtree_name_patterns: list):
#     for pattern in subtree_name_patterns:
#         remote_name = _bigtree.utils.style.name_remote(pattern)
#         r = Bigtree().remote(name=remote_name)
#         commits_ahead = _bigtree.bigtree.remote_commits_ahead(r)
#         print(f"{remote_name} is {commits_ahead} commits ahead of local 'main'.")
#         if commits_ahead > 0:
#             subtrees = [s for s in _bigtree.subtree.create_subtree_factory(pattern)]
#             for s in subtrees:
#                 Bigtree().pull_remote(subtree=s, remote=r)
