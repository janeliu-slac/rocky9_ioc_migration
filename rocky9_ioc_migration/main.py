'''
This script goes into the /configure/RELEASE file of every IOC folder
and updates the module environmental variable to the most recent
EPICS module version found in /cds/group/pcds/epics/R7.0.3.1-2.0/modules/.

Example:
FFMPEGSERVER_MODULE_VERSION = R2.1.1-2.2.2
HISTORY_MODULE_VERSION = R2.7.0
IOCADMIN_MODULE_VERSION = R3.1.16-1.4.0

'''

import json
import os

from get_module_versions import get_module_versions


def main():
    get_module_versions()

    # root is your current working directory
    root = os.path.join(os.path.dirname(__file__), '')
    iocs = []
    module_set = set()

    # Create a list of IOCs that have a /configure/RELEASE file
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)) and '__' not in item:
            subfile = root + item + '/configure/RELEASE'
            if os.path.exists(subfile):
                iocs.append(subfile)

    # Create a set of module environmental variable names retrieved from all
    # IOCs in pcdshub.
    for filepath in iocs:
        if os.path.isfile(filepath):
            with open(filepath, 'r+') as file:
                for line in file:
                    line = ''.join(line.split(' '))
                    if '_MODULE_VERSION=' in line and not line.startswith('#'):
                        mod_name = line.split('=')[0]
                        # put into a set to avoid duplicates
                        module_set.add(mod_name.strip())

    # Outputs module environmental variables currently used in all IOCs to a
    # text file. Can be used to check that env_vars_versions.json has the most
    # recent IOCs.
    with open('env_modules.txt', 'w') as f:
        for item in module_set:
            f.write(str(item) + '\n')

    '''
    The next step in the Rocky 9 migration can't be scripted because certain
    module environmental variables and their EPICS module folder equivalents
    have slightly different names. For example, 'NORMATIVETYPES_MODULE_VERSION'
    and 'normativetypescpp' and 'ETHERCAT_MODULE_VERSION' and 'ethercatmc'.
    There are about 100 module environmental variables used in all IOC
    /configure/RELEASE files, so I manually assigned version numbers to the
    module environmental variables and saved it to a JSON file
    env_vars_versions.json. This JSON file will be used to update all the
    /configure/RELEASE files in IOCs.
    '''

    # If TID builds more modules for the Rocky 9 EPICS base, this script will
    # check for the latest module versions and put it in env_vars_versions.json.
    env_var_dict = {}
    modules_dict = {}

    with open('env_vars_versions.json') as file:
        env_var_dict = json.load(file)

    with open('modules.json') as file:
        modules_dict = json.load(file)

    for env_var in env_var_dict.copy():
        mod_name = (env_var.split('_MODULE_VERSION')[0]).lower()
        if mod_name in modules_dict:
            version = modules_dict[mod_name]
            env_var_dict[env_var] = version

    with open('env_vars_versions.json', 'w') as outfile:
        json.dump(env_var_dict, outfile)

    # Update all IOCs with the latest EPICS module version numbers
    # for each item in EPICS modules directory
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)) and '__' not in item:
            subfile = root + item + '/configure/RELEASE'

            # read the entire RELEASE file
            with open(subfile, 'r') as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = ''.join(line.split(' '))
                    # look for a module environmental variable
                    if '_MODULE_VERSION=' in newline and not line.startswith('#'):
                        env_var = newline.split('=')[0]
                        if env_var in env_var_dict:
                            newline = env_var + ' = ' + env_var_dict[env_var]
                    else:
                        newline = line.strip()
                    newdata.append(newline)

            with open(subfile, 'w') as outfile:
                for line in newdata:
                    outfile.write(line + '\n')


if __name__ == '__main__':
    main()
