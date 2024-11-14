"""
Creates a JSON file (modules.json) containing EPICS module names and
their latest versions. This JSON file will be used to update the
/configure/RELEASE file for every IOC repo.
"""

import json
import os
import re

root = "/cds/group/pcds/epics/R7.0.3.1-2.0/modules"


def check_for_letters(folder):
    # Check all instances where the version folder name has letters in it
    # other than 'FAILED', such as /cds/group/pcds/epics/R7.0.3.1-2.0/modules/xps8/current.
    # This will affect the comparison function that determines the newest
    # version of a module. It is assumed that the module version numbers
    # are all in a format similar to 'R3.1.0-1.4.1'.

    dir = root + "/" + folder

    for ver in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, ver)):
            # check if there is a char other than 'R' in version name
            if "FAILED" not in ver and re.search(r"[a-zA-Z]", ver[1:]):
                print(dir)


def get_newest_version(folder):  # iocAdmin
    dir = root + "/" + folder
    versions = []
    newest = ()

    for ver in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, ver)):
            # Check that 'FAILED' and other chars do not exist in the version
            # name (other than 'R' at the beginning of the string). This
            # assumes that the module version numbers are all in a format
            # similar to 'R3.1.0-1.4.1'.
            if "FAILED" not in ver and not re.search(r"[a-zA-Z]", ver[1:]):
                if "-" in ver:
                    first = ver.split("-")[0]
                    second = ver.split("-")[1]
                    version = (first, second)
                else:
                    version = (ver,)
                versions.append(version)

    if versions:
        newest = versions.pop(0)

        for current in versions:
            if current[0] > newest[0]:
                newest = current
            elif current[0] == newest[0]:
                # check if both have a second version part
                if len(current) > 1 and len(newest) > 1:
                    if current[1] > newest[1]:
                        newest = current
                elif len(current) > 1:
                    newest = current

    return newest


def main():
    modules_dict = {}

    # create a dictionary of module names with their latest versions
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            subdir = item
            version = get_newest_version(subdir)
            if version:
                if len(version) <= 1:
                    modules_dict[subdir] = "".join(version)
                else:
                    modules_dict[subdir] = "-".join(version)

            # (Optional) The function check_for_letters() prints the full path
            # of all folders that contain subfolders with non-standard version
            # names. For example, it will print /cds/group/pcds/epics/R7.0.3.1-2.0/modules/xps8.
            # In /xps8 there is a subfolder named 'current'.

            # check_for_letters(subdir)

    print(modules_dict)

    # write to json file
    with open("modules.json", "w") as outfile:
        json.dump(modules_dict, outfile)


if __name__ == "__main__":
    main()
