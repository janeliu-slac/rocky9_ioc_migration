#!/bin/bash
# Git fork all IOC repos. This script may have to be run several times due
# to limitations on github for how quickly a user can git fork a large
# number of repos. There are 600+ IOC repos.


# Git fork repos that start with "ioc"
gh repo list pcdshub --limit 2000 | while read -r repo _; do
  if [[ $repo == pcdshub/ioc* ]] ;
  then
    gh repo fork "$repo" --default-branch-only --remote
  fi
done
