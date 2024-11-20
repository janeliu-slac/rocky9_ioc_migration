"""
This script goes into the /configure/RELEASE file of every IOC folder
and updates the module environmental variable to the most recent
EPICS module version found in /cds/group/pcds/epics/R7.0.3.1-2.0/modules/.

Example:
FFMPEGSERVER_MODULE_VERSION = R2.1.1-2.2.2
HISTORY_MODULE_VERSION = R2.7.0
IOCADMIN_MODULE_VERSION = R3.1.16-1.4.0

"""

import json
import os

from get_module_versions import get_module_versions


def update_iocs():
    get_module_versions()

    # root is your current working directory
    root = os.path.join(os.path.dirname(__file__), "")
    iocs = []
    module_set = set()

    # Create a list of IOCs that have a /configure/RELEASE file
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)) and "__" not in item:
            subfolder = root + item + "/configure/RELEASE"
            if os.path.exists(subfolder):
                iocs.append(subfolder)

    # Create a python set of module environmental variable names retrieved
    # from all IOCs in pcdshub.
    for filepath in iocs:
        if os.path.isfile(filepath):
            with open(filepath, "r+") as file:
                for line in file:
                    line = "".join(line.split(" "))
                    if "_MODULE_VERSION=" in line and not line.startswith("#"):
                        mod_name = line.split("=")[0]
                        # put into a set to avoid duplicates
                        module_set.add(mod_name.strip())

    # Output module environmental variables currently used in all IOCs to a
    # text file.
    with open("env_modules.txt", "w") as f:
        for item in module_set:
            f.write(str(item) + "\n")

    """
    The next step in the Rocky 9 migration can't be scripted because certain
    module environmental variables and their EPICS module folder equivalents
    have slightly different names. For example, 'NORMATIVETYPES_MODULE_VERSION'
    and 'normativetypescpp' and 'ETHERCAT_MODULE_VERSION' and 'ethercatmc'.
    In the 600+ IOCs there are about 100 module environmental variables used in
    /configure/RELEASE files, so I manually assigned version numbers to the
    module environmental variables and saved it to a JSON file
    env_vars_versions.json. This JSON file will be used to update all the
    /configure/RELEASE files in IOCs.
    """

    with open("env_vars_versions.json") as file:
        mod_ver_dict = json.load(file)

    # Update all IOCs with the latest EPICS module version numbers
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)) and "__" not in item:
            subfolder = root + item + "/configure/RELEASE"
            print(subfolder)

            # read the entire file
            with open(subfolder, "r+") as file:
                data = file.readlines()

                for i, line in enumerate(data.copy()):
                    line = "".join(line.split(" "))

                    # look for a module environmental variable
                    if "_MODULE_VERSION=" in line:
                        env_var = line.split("=")[0]
                        if env_var in mod_ver_dict:
                            ver = mod_ver_dict[env_var]
                            data[i] = env_var + " = " + ver
                            print(data[i])


if __name__ == "__main__":
    update_iocs()
