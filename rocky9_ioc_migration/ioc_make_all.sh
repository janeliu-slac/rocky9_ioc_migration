#!/bin/bash

##############################################################################
# REQUIRES UPDATE: Give the 'branch_name' variable a new git branch name
##############################################################################
branch_name="rocky9_master"

##### Runs 'make' on all IOCs. If IOC builds without errors, open a PR.
error_log="$(pwd)/error.log"

rm "$error_log"
touch "$error_log"

# Go up into ../../iocs folder
cd ../..

for dir in */; do
    if [ -d "$dir" ]; then
        (
            cd "$dir"
            echo -e "\e[1;35m$dir.\e[0m"
            git checkout $branch_name
            make distclean
            make
            {
                echo -e \"\n\"
                pwd
            } >>$error_log
            make 2>>$error_log
            if [ $? -ne 0 ]; then
                echo "An error occurred during make. See error.log for details."
            else
                echo "Make completed successfully. Opening a pull request."
                # gh pr create --head --title "ECS-6549 Build and release IOCs for Rocky 9" --body "Updated configuration files for Rocky 9 migration."
            fi
            cd ..
            sleep 2
        )
    fi
done
