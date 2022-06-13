from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Union

import git
import git.cmd
from git import HEAD, Blob, Commit, GitCommandError, Remote, Repo, Tree

import _bigtree.utils.style
from _bigtree.config import BigtreeReader
from _bigtree.exceptions import ProtectedBranchError
from _bigtree.subtree import Subtree
from _bigtree.utils import Constants


def is_default_branch(head: HEAD, fail_quietly=False):
    """A basic sanity check."""
    branch_name = head.reference.name
    default_branch_name = Constants.DEFAULT_BRANCH

    if branch_name == default_branch_name:
        return True
    elif fail_quietly is False:
        error_msg = (
            f"Branch '{branch_name}' does not appear to be the default "
            + f"branch (expected default branch name is '{default_branch_name}')."
        )
        raise ValueError(error_msg)
    else:
        # don't raise an exception, but still return False
        return False


def remote_commits_ahead(remote: Remote) -> int:
    """"""
    # git rev-list --left-right --count python_remote/main...main
    working_dir = _bigtree.utils.get_bigtree_root()
    default_branch_name = Constants.DEFAULT_BRANCH
    g = git.cmd.Git(working_dir)
    # TODO: Fix this so we use subtree.remote_branch instead of default_branch_name.
    cmd = f"git rev-list --left-right --count {remote.name}/{default_branch_name}...{default_branch_name}"
    try:
        output = g.execute(command=(cmd.split(" ")))
    except GitCommandError as e:
        print(e.with_traceback(None))

    commits_ahead = output.split("\t")[0]
    return int(commits_ahead)


@dataclass
class BigtreeGitData:
    """"""

    protected_branches: list[str]


class BigtreeGit:
    """"""

    # TODO: Make a base class so we don't have this duplicated
    root_dir = Constants.BIGTREE_DIR

    def __init__(self) -> None:
        self._gitdata = BigtreeGitData(
            protected_branches=BigtreeReader().get("protect_branches"),
        )
        self._repo = Repo(self.root_dir)

    @property
    def active_branch(self):
        """Returns the currently active branch."""
        return self._repo.head

    @property
    def active_branch_name(self):
        """Returns the name of the currently active branch."""
        return self.active_branch.reference.name

    @property
    def blobs(self) -> list[Blob]:
        return self._repo.heads.main.commit.tree.blobs

    @property
    def branches(self):
        return self._repo.heads

    @property
    def branches_remote(self):
        return self._repo.remote().refs

    @property
    def files(self) -> list[str]:
        return [blob.name for blob in self.blobs]

    @property
    def latest_commit(self) -> Commit:
        return self._repo.commit()

    @property
    def main(self) -> HEAD:
        """Returns the default branch."""
        main_branch_name = Constants.DEFAULT_BRANCH
        for branch in self.branches:
            name = branch.name if branch.name != "HEAD" else branch.reference.name
            if name == main_branch_name:
                return branch
        raise ValueError(f"No branch found with name '{main_branch_name}'.")

    @property
    def main_branch_name(self) -> str:
        """Returns the name of the default branch."""
        name = self.main.name if self.main.name != "HEAD" else self.main.reference.name
        return name

    @property
    def protected_branches(self):
        return self._gitdata.protected_branches

    @property
    def remote_name_dict(self) -> dict:
        remotes_dict = {}
        for remote in self.remotes_list:
            remotes_dict[remote.name] = remote
        return remotes_dict

    @property
    def remote_url_dict(self) -> dict:
        remotes_dict = {}
        for remote in self.remotes_list:
            remotes_dict[remote.url] = remote
        return remotes_dict

    @property
    def remotes_iter(self) -> Iterator[Remote]:
        self._repo = Repo(self.root_dir)
        return git.Remote.iter_items(repo=self._repo)

    @property
    def remotes_list(self) -> list[Remote]:
        self._repo = Repo(self.root_dir)
        return git.Remote.list_items(repo=self._repo)

    @property
    def repo(self) -> Repo:
        return self._repo

    @property
    def subdirectories(self) -> list[str]:
        return [tree.name for tree in self.trees]

    @property
    def trees(self) -> list[Tree]:
        return self._repo.heads.main.commit.tree.trees

    def branch(self, name=None):
        """Given a `name`, return the corresponding `Branch` object."""

        branches_dict = {}
        for branch in self.branches:
            bname = branch.name if branch.name != "HEAD" else branch.reference.name
            branches_dict[bname] = branch
        for branch in self.branches_remote:
            bname = branch.name if branch.name != "HEAD" else branch.reference.name
            branches_dict[bname] = branch
        return branches_dict

    def remote(self, name: str = None, url: str = None) -> Remote:
        """Given a `name` or `url`, return the corresponding `Remote` object.

        Raises `KeyError if name or url isn't found.
        """
        if not name and not url:
            raise TypeError("get_remote() requires either a 'name' or 'url'.")
        elif name and url:
            raise TypeError(
                "get_remote() requires either a 'name' or 'url', "
                + "but it cannot take both!"
            )
        elif name and not url:
            return self.remote_name_dict[name]
        else:  # url and not name
            return self.remote_url_dict[url]

    def add_remote(self, remote_name: str, remote_url: str, prefix: Union[str, Path]):
        if _bigtree.utils.style.is_remote_name_valid(remote_name) is False:
            raise ValueError(
                "The remote_name should end in '-remote', "
                + f"but remote_name is {remote_name} instead."
            )

        p = prefix
        if isinstance(p, str):
            if p.startswith("/"):
                p = Path(p).name
        else:
            # p is Path
            p = p.relative_to(self.root_dir)

        return self._repo.create_remote(name=remote_name, url=remote_url)

    def delete_remote(self, remote: Union[Remote, str]):
        while isinstance(remote, str):
            r: Remote = self.remotes_iter
            remote = r if r.name == remote else remote
        return self._repo.delete_remote(remote)

    def pull_remote(self, subtree: Subtree, remote: Remote, commit_msg: str = None):
        """"""
        # check to make sure active branch isn't protected
        if self.active_branch_name in self.protected_branches:
            raise ProtectedBranchError(
                branch_name=self.active_branch_name,
                request_description=f"pull remote {Remote.name}",
            )

        # construct 'git subtree pull' command
        prefix_flag = f"--prefix={subtree.local_directory(absolute=False)}"
        rname = remote.name
        rbranch = subtree.remote_branch
        if commit_msg:
            msg_flag = f'-m "{_bigtree.utils.style.commit_message(commit_msg)}"'
        else:
            msg_flag = f'-m "{_bigtree.utils.style.commit_message_merge(remote)}"'
        cmd = ["git", "subtree", "pull", "-d", prefix_flag, rname, rbranch, msg_flag]

        # run 'git subtree pull' command, with some print()s for debug :)
        # TODO: proper debugging with --verbose flag
        print(cmd)
        g = git.cmd.Git(Constants.BIGTREE_DIR)
        try:
            output = g.execute(command=cmd)
            print(output)
        except GitCommandError as e:
            print(e.with_traceback(None))
