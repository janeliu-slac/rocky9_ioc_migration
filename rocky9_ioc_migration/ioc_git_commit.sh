#!/bin/bash

# This script will create a new branch called 'ECS-6549', commit all changes 
# made after running main.py, and create a PR for the forked repo.

BRANCH_NAME="ECS-test"

# List of repositories
REPOS=(
    "ioc-common-ads-ioc"
    "ioc-common-bk-1697"
    "ioc-common-epixMon"
)

# Create the branch in each repository
for repo in "${REPOS[@]}"; do

    cd "$repo" || exit 1

    if [[ `git status --short` ]]; then
        git status --porcelain
    fi

    cd .. || exit 1

    # echo "Creating branch '$BRANCH_NAME' in repository '$repo'"
    # cd "$repo" || exit 1
    # git checkout -b "$BRANCH_NAME"
    
done