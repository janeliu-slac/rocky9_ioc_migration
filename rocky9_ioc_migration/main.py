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

epics_base_version = 'R7.0.3.1-2.0'


def main():
    get_module_versions()

    # root is your current working directory
    root = os.path.join(os.path.dirname(__file__), '')
    iocs_config_release = []
    iocs_release_site = []
    module_set = set()

    # Create lists of IOCs that have /configure/RELEASE and RELEASE_SITE files
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)) and '__' not in item:
            file_config_release = root + item + '/configure/RELEASE'
            file_release_site = root + item + '/RELEASE_SITE'

            if os.path.exists(file_config_release):
                iocs_config_release.append(file_config_release)

            if os.path.exists(file_release_site):
                iocs_release_site.append(file_release_site)

    # Create a set of module environmental variables
    for filepath in iocs_config_release:
        if os.path.isfile(filepath):
            with open(filepath, 'r+') as file:
                for line in file:
                    line = ''.join(line.split(' '))
                    if '_MODULE_VERSION=' in line and not line.startswith('#'):
                        mod_name = line.split('=')[0]
                        # put into a set to avoid duplicates
                        module_set.add(mod_name.strip())

    '''
    The next step in the Rocky 9 migration can't be scripted because certain
    module environmental variables and their EPICS module folder equivalents
    have slightly different names. For example, 'NORMATIVETYPES_MODULE_VERSION'
    and 'normativetypescpp' and 'ETHERCAT_MODULE_VERSION' and 'ethercatmc'.
    There are 100+ module environmental variables used in all IOC
    /configure/RELEASE files. I generated a list of all module environmental
    variables, manually assigned version numbers when needed, and saved it to
    a JSON file (env_vars_versions.json). This JSON file will be used to
    update all /configure/RELEASE files in IOCs.
    '''

    # Check for any new module environmental variables in IOCs and add them to
    # env_vars_versions.json. If TID builds more modules for the Rocky 9 EPICS
    # base, this script will add them to env_vars_versions.json.
    env_var_dict = {}
    modules_dict = {}

    with open('env_vars_versions.json') as file:
        env_var_dict = json.load(file)

    with open('modules.json') as file:
        modules_dict = json.load(file)

    for var in module_set:
        if var not in env_var_dict:
            env_var_dict[var] = ''

    for env_var in env_var_dict.copy():
        mod_name = (env_var.split('_MODULE_VERSION')[0]).lower()

        # Newest MOTOR_MODULE_VERSION = R6.9-ess-0.0.1 and does not conform to
        # semantic versioning. TID (Jeremy) mentioned there may be special
        # changes in R6.9-ess-0.0.1 that are needed for ioc-common-ads-ioc. So,
        # here the code does not update MOTOR_MODULE_VERSION.

        if mod_name in modules_dict and modules_dict[mod_name] and mod_name != 'motor':
            version = modules_dict[mod_name]
            env_var_dict[env_var] = version

    with open('env_vars_versions.json', 'w') as outfile:
        json.dump(env_var_dict, outfile)

    # Update all IOCs with the latest EPICS module version numbers
    for filepath in iocs_config_release:
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = line.replace('\t', '').strip()
                    newline = ''.join(newline.split(' '))

                    # look for a module environmental variable
                    if '_MODULE_VERSION=' in newline and not line.startswith('#'):
                        env_var = newline.split('=')[0]
                        version = newline.split('=')[1]
                        if env_var_dict[env_var]:
                            version = env_var_dict[env_var]
                        newline = env_var + ' = ' + version
                        newdata.append(newline.strip())
                    else:
                        newdata.append(line.strip())

            with open(filepath, 'w') as outfile:
                for line in newdata:
                    outfile.write(line + '\n')

    # Update all IOCs with the new EPICS base version number
    for filepath in iocs_release_site:
        if os.path.isfile(filepath):
            with open(filepath, 'r+') as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = line.replace('\t', '').strip()
                    newline = ''.join(newline.split(' '))

                    if 'BASE_MODULE_VERSION=' in line and not line.startswith('#'):
                        newline = 'BASE_MODULE_VERSION = ' + epics_base_version
                        newdata.append(newline.strip())
                    else:
                        newdata.append(line.strip())

            with open(filepath, 'w') as outfile:
                for line in newdata:
                    outfile.write(line + '\n')


if __name__ == '__main__':
    main()
