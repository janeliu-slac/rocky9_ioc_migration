'''
Creates a JSON file (modules.json) containing EPICS module names and
their latest versions. This JSON file will be used to update the
/configure/RELEASE file for every IOC repo.
'''

import json
import os
import re

from packaging import version

root = '/cds/group/pcds/epics/R7.0.3.1-2.0/modules'


def compare_versions(ver1, ver2):
    v1 = version.parse(ver1)
    v2 = version.parse(ver2)

    if v1 > v2:
        return ver1
    elif v1 < v2:
        return ver2
    else:
        return 'same'


def get_newest_version(folder):
    # Checks in an EPICS module folder and reads its subfolder names
    # (subfolder names use semantic versioning). Returns the latest
    # version.

    dir = root + '/' + folder
    newest = ()
    versions = []

    for ver in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, ver)):
            # Check that 'FAILED' and other chars do not exist in the version
            # name (other than 'R' at the beginning of the string). This
            # assumes that the module version numbers are all in a format
            # similar to 'R3.1.0-1.4.1'.
            if 'FAILED' not in ver and not re.search(r'[a-zA-Z]', ver[1:]):
                if '-' in ver:
                    first = ver.split('-')[0][1:]
                    second = ver.split('-')[1]
                    version = (first, second)
                else:
                    version = (ver.split('-')[0][1:],)
                versions.append(version)

    if versions:
        newest = versions.pop(0)
        for current in versions:
            result = compare_versions(newest[0], current[0])
            if result == current[0]:
                newest = current
            elif result == 'same':
                # check if both have a second version part
                if len(current) > 1 and len(newest) > 1:
                    result = compare_versions(newest[1], current[1])
                    if result == current[1]:
                        newest = current
                elif len(current) > 1:
                    newest = current

    return newest


def get_module_versions():
    # Creates a JSON file containing EPICS module names and their latest
    # versions.

    modules_dict = {}

    # create a dictionary of module names with their latest versions
    for subfolder in os.listdir(root):
        if os.path.isdir(os.path.join(root, subfolder)):
            latest_ver = get_newest_version(subfolder)
            if latest_ver:
                # save to the dictionary in lowercase for easy lookup later
                subfolder = subfolder.lower()
                if len(latest_ver) <= 1:
                    num = ''.join(latest_ver)
                else:
                    num = '-'.join(latest_ver)

                modules_dict[subfolder] = 'R' + num

    # write to json file
    with open('modules.json', 'w') as outfile:
        json.dump(modules_dict, outfile)
