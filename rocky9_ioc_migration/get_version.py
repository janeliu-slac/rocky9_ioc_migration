"""
Creates a JSON file (modules.json) containing EPICS module names and
their latest versions. This JSON file will be used to update the
/configure/RELEASE file for every IOC repo.

1. Get every subdirectory name in /cds/group/pcds/epics/R7.0.3.1-2.0/modules.

2. cd into every subdirectory, read the name of each folder (folder name is
the version number), and find the folder with the latest version.

3. Store the subdirectory name and the latest version as a key-value pair
   in modules.json.

"""

import json
import os

root = "/cds/group/pcds/epics/R7.0.3.1-2.0/modules"


def get_newest_version(folder):  # iocAdmin
    dir = root + "/" + folder
    versions = []

    for item in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, item)):
            ver = item
            if "FAILED" not in ver:
                if "-" in ver:
                    first = ver.split("-")[0]
                    second = ver.split("-")[1]
                    version = (first, second)
                else:
                    version = (ver,)
                versions.append(version)

    if versions:
        newest = versions.pop(
            0
        )  # remove first element in versions and assign to newest
        for current in versions:
            if current[0] > newest[0]:  # compare first version part
                newest = current
            elif (
                current[0] == newest[0]
            ):  # if current is R3.1.16 and newest is R3.1.16-1.2.0
                # check if both have a second version part
                if len(current) > 1 and len(newest) > 1:  # false
                    if current[1] > newest[1]:
                        newest = current
                elif len(current) > 1:  # false
                    newest = current

    return newest


def main():
    modules_dict = {}

    # create a dictionary of module names with their latest versions
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            subdir = item
            ver = get_newest_version(subdir)
            modules_dict[subdir] = ver

    print(modules_dict)

    # write to json file
    with open("modules.json", "w") as outfile:
        json.dump(modules_dict, outfile)


if __name__ == "__main__":
    main()
