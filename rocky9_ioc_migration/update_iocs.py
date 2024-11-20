"""
This script goes into the /configure/RELEASE file of every IOC folder
and updates the module environmental variable to the most recent
EPICS module version found in /cds/group/pcds/epics/R7.0.3.1-2.0/modules/.

Example:
FFMPEGSERVER_MODULE_VERSION = R2.1.1-2.2.2
HISTORY_MODULE_VERSION = R2.7.0
IOCADMIN_MODULE_VERSION = R3.1.16-1.4.0

"""

import os

from get_module_versions import get_module_versions


def update_iocs():
    get_module_versions()

    # root is your current working directory
    root = os.path.join(os.path.dirname(__file__), "")
    iocs = []
    module_set = set()
    env_vars = {}
    env_var_with_versions = {}

    # Create a list of IOCs that have a /configure/RELEASE file
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            subfolder = root + item + "/configure/RELEASE"
            if os.path.exists(subfolder):
                iocs.append(subfolder)

    # Create a list (set) of module environmental variable names based
    # on all IOCs in pcdshub.
    for filepath in iocs:
        if os.path.isfile(filepath):
            with open(filepath, "r+") as file:
                for line in file:
                    if "_MODULE_VERSION=" in line and not line.startswith("#"):
                        mod_name = line.split("=")[0]
                        # put into a set to avoid duplicates
                        module_set.add(mod_name.strip())

    # Generate a text file with a list of all the module environmental variables
    # that currently appear in the /configure/RELEASE file of every IOC folder.
    with open("module_environ_vars.txt", "w") as file:
        for var in module_set:
            file.write(f"{var}\n")

    """
    The rest of the migration can't be scripted because certain module
    environmental variables and their EPICS module folder equivalents
    are named differently. For example, 'NORMATIVETYPES_MODULE_VERSION'
    and 'normativetypescpp'. The total number of module environmental
    variables that show up in all IOC /configure/RELEASE files is less
    than 70, so I manually assigned version numbers to the module
    environmental variables and saved it to module_versions_edited.txt.
    """

    mod_ver_dict = {}

    # Create a dictionary based on the manually updated file
    with open("modules_versions_edited.txt", "r") as file:
        for line in file:
            line = "".join(line.split(" "))
            if "_MODULE_VERSION=" in line:
                env_var = line.split("=")[0]
                ver = (line.split("=")[1]).strip()
                mod_ver_dict[env_var] = ver

    # Update all IOCs with the latest version of EPICS modules
    for item in os.listdir(root):
        if os.path.isdir(os.path.join(root, item)):
            subfolder = root + item + "/configure/RELEASE"
            # read the entire file
            with open(subfolder, "r+") as file:
                data = file.readlines()
                for i, line in enumerate(data):
                    line = "".join(line.split(" "))
                    # look for a module environmental variable
                    if "_MODULE_VERSION=" in line:
                        env_var = line.split("=")[0]
                        if env_var in mod_ver_dict:
                            ver = mod_ver_dict[env_var]
                            data[i] = env_var + " = " + ver


if __name__ == "__main__":
    update_iocs()
