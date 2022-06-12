# notes on Git subtrees

Notes taken from: 
- https://www.howtogeek.com/devops/how-to-use-git-subtree-to-manage-multiple-project-repositories/
- https://betterprogramming.pub/git-subtree-usage-6aaba8b5d947

## Creating subtrees

In order to create a subtree in an existing project, first add the subtree repository as a remote repository and fetch the commit history.

```
git remote add --fetch SubtreeName https://github.com/user/SubtreeProject.git
```

Then, add the remote repository as a subtree, locating it in a new directory (`--prefix`). Note that the directory named in `--prefix` will be created by this command, so it can't already exist. Also note that the `--squash` flag is optional. It's often used in order to keep the commit history of the parent repository clean, but we're not going to use it in this repository since its main purpose is to track changes made across these similar repositories.

```
git subtree add --prefix desired/path/to/subtree SubtreeName BranchName --squash
```

## Using subtrees

Using subtrees is a bit of a complex process, unfortunately. In order to pull in new commits from the subtree's remote repository, you have to type:

```
git fetch SubtreeName BranchName

git subtree pull --prefix desired/path/to/subtree SubtreeName SubtreeName master --squash
```
