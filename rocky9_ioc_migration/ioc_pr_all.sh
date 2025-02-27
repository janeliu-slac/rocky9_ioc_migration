#!/bin/bash

##############################################################################
# REQUIRES UPDATE: Give the 'branch_name' variable a new git branch name
##############################################################################
branch_name="rocky9_master"

# Go up into ../../iocs folder
cd ../..

##### Runs 'make' on all IOCs. If IOC builds without errors, open a PR.
date_string=$(date +%Y%m%d_%H%M%S)
error_log="error_${date_string}.log"
touch "$error_log"

for dir in */; do
  if [ -d "$dir" ]; then
    (
      cd "$dir"
      pwd
      git checkout $branch_name
      make_distclean
      make
      if [ $? -ne 0 ]; then
        (
          {
            echo -e \"\n\"
            pwd
          } >>$error_log
          make 2>>$error_log
        )
      else
        gh pr create --head --title "ECS-6549 Build and release IOCs for Rocky 9" --body ""
      fi
      cd ..
      sleep 2
    )
  fi
done
