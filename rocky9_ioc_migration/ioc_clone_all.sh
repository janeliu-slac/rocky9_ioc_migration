#!/bin/bash

# Git clone the forked common IOC repos into /iocs

gh repo list janeliu-slac --limit 2000 | while read -r repo _; do
  if [[ $repo == janeliu-slac/ioc-common* ]] ;
  then
    cd ../..
    gh repo clone "$repo"
  fi
done
