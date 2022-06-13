#!/bin/bash
# Usage:
#   ./update.sh <subtree name>
#
# This script is a modified version of Roy Williamse's script from 
# the end of this post:
#   https://sourcefield.nl/post/git-subtree-survival-tips/

# Check if being called just to display --help
if "$1" == "--help"; then 
    # print help message and exit this script
    echo "A simple script to update a repository's subtrees."
    echo ""
    echo "Usage:"
    echo "  ./update.sh <branch or tag (defaults to 'main')>"
    exit 0
fi

# example: debian_remote
remote="$1_remote"
# example: alemna/debian
remote_image="alemna/$1" 
# example: https://github.com/alemna-docks/debian.git
subtree_repo="https://github.com/alemna-docks/$1.git"
# Where to mount the subtree
folder="$1" # example: debian

echo "ADDING REMOTE '$remote'"
git remote add $remote --no-tags $subtree_repo
git fetch $remote main
starting_commit=$(git rev-parse --verify HEAD)
remote_latest_commit=$(git rev-parse --verify FETCH_HEAD)

git stash
if [[ -d $folder ]]; then 
    # update the existing subtree
    echo "$folder FOLDER EXISTS, UPDATING SUBTREE"
    git subtree split --prefix=debian --annotate='(split) ' --rejoin --branch test
    #git subtree pull $remote main \
    #--prefix=$folder -m "Update from '$remote' at '$remote_latest_commit'"
else 
    # add the subtree
    echo "$folder FOLDER DOES NOT EXIST, ADDING SUBTREE"
    git subtree add  $remote main --prefix=$folder \
    -m "Add '$folder'/ from '$remote' at '$remote_latest_commit'"
fi

new_commit=$(git rev-parse --verify HEAD)
# 'git diff --name-only $starting_commit $new_commit | wc --lines' overcounts
# files changed by 1, so subtract 1
files_changed=$(($(git diff --name-only $starting_commit $new_commit | wc --lines)-1))
echo "FILES CHANGED: $files_changed"

if [[ $files_changed -gt 0 ]]; then
    # If files have changed, then push a commit, build new images, and
    # push the new images to the docker repository
    echo "PUSHING CHANGES IN GIT..."
    git push origin main

    echo "BUILDING AND PUSHING IMAGES..."
    cd $folder
    docker compose up --build
    docker push --all-tags $remote_image
else
    echo "NO CHANGES, NO NEW IMAGES NEEDED."
fi

git remote remove $remote
