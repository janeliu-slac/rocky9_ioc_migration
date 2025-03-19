#!/bin/bash

# Git clone the forked common IOC repos into /iocs

# update this with your Github username
github_username=janeliu-slac
username_len=${#github_username} # get length of github_username

cd ../..

gh repo list $github_username --limit 2000 | while read -r repo _; do
  if [[ $repo == $github_username/ioc-common* ]]; then
    ioc_name="${repo:$username_len}" # truncate the github_username to get IOC repo name and clone it into your dev environment
    gh repo clone "$repo" "$ioc_name"
    sleep 1
  fi
done
