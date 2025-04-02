#!/bin/bash

##############################################################################
# REQUIRES UPDATE: Change the 'user' and 'branch_name' variables
##############################################################################
branch_name="rocky9_master"

##### Runs 'make' on all IOCs. If IOC builds without errors, open a git PR.

export HOME_DIR="$(
    cd "$(dirname "${BASH_SOURCE[0]}")"
    pwd -P
)"
error_log="$HOME_DIR/error.log"
not_building="$HOME_DIR/does_not_build.txt"
building="$HOME_DIR/builds_correctly.txt"

rm "$error_log"
rm "$not_building"
touch "$error_log"
touch "$not_building"
sleep 3

# Go up into /iocs folder
cd ../..

for dir in */; do
    if [ -d "$dir" ]; then
        (
            cd "$dir"
            echo -e "\e[1;35m$dir\e[0m"
            git checkout $branch_name
            git push --set-upstream origin $branch_name
            make distclean
            make
            {
                echo -e "\\n"
                pwd
            } >>$error_log
            make 2>>$error_log
            if [ $? -ne 0 ]; then
                printf "\nFailure. An error occurred during make. See error.log for details.\n"
                echo -e "$dir" >>$not_building
            else
                echo -e "$dir" >>$building
                printf "\nSuccessfully ran 'make'. Attempting to open a pull request.\n"
                gh repo set-default git@github.com:pcdshub/$dir.git
                gh pr create --title "ECS-6549 Build and release IOCs for Rocky 9" --body "Updated configuration files for Rocky 9 migration."
            fi
            cd ..
            sleep 2
        )
    fi
done
