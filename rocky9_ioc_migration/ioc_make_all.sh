#!/bin/bash

# This script has multiple functions:
# 1. Git fetch and rebase master for all common IOCs.
# 2. Checks if configure/RELEASE and RELEASE_SITE files have been modified
#    in each IOC. If so, git add and commit files and push to remote.
# 3.

##############################################################################
# REQUIRES UPDATE: Give the 'branch_name' variable a new git branch name
##############################################################################
branch_name="rocky9_master"

release_file="RELEASE"
release_local_file="RELEASE.local"
release_site_file="RELEASE_SITE"

# Specify the commands to execute
error_log="$(pwd)/error.log"

# Go up into ../../iocs folder
cd ../..

##### Copy all changes from master to the new branch ($branch_name)
##### (Use this if you accidentally make changes to master instead
##### of the new branch)
# find . -maxdepth 2 -type d -name .git -exec sh -c "cd \"{}\"/../ && \
# pwd && \
# git stash && \
# git checkout -b $branch_name && \
# git stash apply && \
# sleep 2" \;

# #### Git fetch upstream and rebase master
# for dir in */; do
#     if [ -d "$dir" ]; then
#         (
#             cd "$dir"
#             pwd
#             git checkout $branch_name
#             git stash
#             git checkout master
#             git fetch upstream
#             git rebase upstream/master
#             sleep 2
#             git push -f
#             sleep 2
#             git checkout $branch_name
#             git rebase master
#             git push --set-upstream origin $branch_name -f
#             git stash pop
#             cd ..
#             sleep 3
#         )
#     fi
# done

##### Git add/commit/push configure/RELEASE and RELEASE_SITE files
for dir in */; do
    if [ -d "$dir" ]; then
        (
            cd "$dir"
            pwd
            git checkout $branch_name
            if [ -f "$release_site_file" ]; then
                git diff --quiet "$release_site_file"
                if [ $? -ne 0 ]; then
                    git add "$release_site_file"
                    git commit -m "Updated $release_site_file"
                    echo "Updated $dir $release_site_file."
                fi
            fi
            # if [ -d "configure" ]; then
            #     cd configure
            #     if [ -f "$release_file" ]; then
            #         git diff --quiet "$release_file"
            #         if [ $? -ne 0 ]; then
            #             git add "$release_file"
            #             git commit -m "Updated $release_file"
            #             echo "Updated $dir configure/$release_file with newest module version numbers."
            #         fi
            #     fi
            #     if [ -f "$release_local_file" ]; then
            #         git diff --quiet "$release_local_file"
            #         if [ $? -ne 0 ]; then
            #             git add "$release_local_file"
            #             git commit -m "Updated $release_local_file"
            #             echo "Updated $dir configure/$release_local_file with newest module version numbers."
            #         fi
            #     fi
            #     cd ..
            # fi
            # cd ..
            # git push --set-upstream origin $branch_name
            sleep 1
        )
    fi
done

# ##### Run 'make' on each IOC and output compilation errors to an error log file

# find . -maxdepth 2 -type d -name .git -exec sh -c "cd \"{}\"/../ && \
# make_distclean && \
# make && \
# { echo -e \"\n\"; pwd; } >> $error_log && \
# make 2>> $error_log && \
# sleep 2" \;

## TO-DO: Open git PR
