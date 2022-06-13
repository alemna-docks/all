#!/bin/bash
# Returns the most recent commit to touch a directory.

git log --pretty=%H --max-count=1 $1
