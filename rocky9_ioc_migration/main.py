'''
This script goes into the /configure/RELEASE file of every IOC folder
and updates the module environmental variable to the most recent
EPICS module version found in /cds/group/pcds/epics/R7.0.3.1-2.0/modules/.

Example:
FFMPEGSERVER_MODULE_VERSION = R2.1.1-2.2.2
HISTORY_MODULE_VERSION = R2.7.0
IOCADMIN_MODULE_VERSION = R3.1.16-1.4.0

NOTE: ioc-common-ads-ioc should be updated manually. This IOC does not use the
same EPICS module versions as other IOCs.
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
                    newline = line.replace('\t', '').strip()
                    newline = ''.join(newline.split(' '))

                    if '_MODULE_VERSION=' in newline and not line.startswith('#'):
                        mod_name = newline.split('=')[0]
                        # put into a set to avoid duplicates
                        module_set.add(mod_name.strip())

    '''
    The next step in the Rocky 9 migration can't be scripted because certain
    module environmental variables and their EPICS module folder equivalents
    have slightly different names. For example, 'ETHERCAT_MODULE_VERSION' and 
    'ethercatmc'. There are 100+ module environmental variables used in all IOC
    /configure/RELEASE files. I generated a list of all module environmental
    variables, manually assigned version numbers when needed (and wherever a
    different version number is indicated in the PCDS Rocky 9 Build Status page
    in Confluence), and saved it to a JSON file (env_vars_versions.json). This
    JSON file will be used to update all /configure/RELEASE files in IOCs.

    These environmental variables and EPICS modules have slightly different 
    spelling. They should be updated by hand (not a complete list):
    'ETHERCAT_MODULE_VERSION' --> 'ethercatmc'
    'NORMATIVETYPES_MODULE_VERSION' --> 'normativetypescpp'
    'STREAM_MODULE_VERSION' --> 'streamdevice'

    These modules are using an older version (not the latest):
    'STREAMDEVICE_MODULE_VERSION' and 'STREAM_MODULE_VERSION' --> R2.8.9-1.2.2
    'IPAC_MODULE_VERSION' --> R2.15-1.0.2

    '''

    # Load env_vars_versions.json
    env_var_dict = {}
    modules_dict = {}

    with open('env_vars_versions.json') as file:
        env_var_dict = json.load(file)

    with open('modules.json') as file:
        modules_dict = json.load(file)

    # Update env_vars_versions.json with the newest EPICS module version
    # numbers. Check PCDS Rocky 9 Build Status Confluence page 'Notes'
    # column for modules that should be using an earlier version.
    for key in env_var_dict.copy():
        env_var_lower = (key.split('_MODULE_VERSION')[0]).lower()
        if env_var_lower in modules_dict:
            env_var_dict[key] = modules_dict[env_var_lower]

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

                    if 'BASE_MODULE_VERSION=' in newline and not line.startswith('#'):
                        newline = 'BASE_MODULE_VERSION = ' + epics_base_version
                        newdata.append(newline.strip())
                    elif 'EPICS_SITE_TOP=' in newline and not line.startswith('#'):
                        newline = 'EPICS_SITE_TOP = /cds/group/pcds/epics'
                        newdata.append(newline.strip())
                    elif 'PSPKG_ROOT=' in newline and not line.startswith('#'):
                        newline = 'PSPKG_ROOT = /cds/group/pcds/pkg_mgr'
                        newdata.append(newline.strip())
                    else:
                        newdata.append(line.strip())

            with open(filepath, 'w') as outfile:
                for line in newdata:
                    outfile.write(line + '\n')


if __name__ == '__main__':
    main()
    # subprocess.call('ioc_git_commit.sh')
