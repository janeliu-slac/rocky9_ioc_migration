#!/bin/bash

# Git clone the forked common IOC repos into /iocs

# update this with your Github username
github_username=janeliu-slac

cd ../..

gh repo list $github_username --limit 2000 | while read -r repo _; do
  gh repo clone "$repo" "$repo"
  sleep 2
done
