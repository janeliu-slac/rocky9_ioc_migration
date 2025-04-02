# Scripts to fix various bugs

import json
import os


def replace_autosavedbd():
    app_src_makefiles = []
    names = []
    file_app_src_makefile1 = ""
    file_app_src_makefile2 = ""

    parent = os.path.dirname(os.path.join(os.path.dirname(__file__), ""))
    grandparent = os.path.dirname(parent)
    greatgrandparent = os.path.dirname(grandparent)

    # Create lists of IOCs that have app/src/Makefile files
    for item in os.listdir(greatgrandparent):
        if os.path.isdir(os.path.join(greatgrandparent, item)) and "__" not in item:
            file_app_src_makefile1 = greatgrandparent + "/" + item + "/app/src/Makefile"

            if os.path.exists(file_app_src_makefile1):
                app_src_makefiles.append(file_app_src_makefile1)

            name = item.split("-")
            ioc_name = ""

            try:
                name[3]
                ioc_name = name[2]
                for word in name[3:]:
                    ioc_name += "-" + word
                names.append(ioc_name)
                file_app_src_makefile2 = greatgrandparent + "/" + \
                    item + "/" + ioc_name + "App/src/Makefile"
                if os.path.exists(file_app_src_makefile2):
                    app_src_makefiles.append(file_app_src_makefile2)
            except IndexError:
                pass

            try:
                names.append(name[2])
                file_app_src_makefile2 = greatgrandparent + "/" + \
                    item + "/" + name[2] + "App/src/Makefile"
                if os.path.exists(file_app_src_makefile2):
                    app_src_makefiles.append(file_app_src_makefile2)
            except IndexError:
                pass

    for filepath in app_src_makefiles:
        if os.path.isfile(filepath):
            with open(filepath, "r+") as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = line.replace("\t", "").strip()
                    newline = "".join(newline.split(" "))

                    if "autosaveSupport.dbd" in newline and not line.startswith("#"):
                        newline = line.replace(
                            "autosaveSupport.dbd", "asSupport.dbd")
                        newdata.append(newline.strip())

                    else:
                        newdata.append(line.strip())

            with open(filepath, "w") as outfile:
                for line in newdata:
                    outfile.write(line + "\n")


def replace_RULEScopy():
    # In app/srcProtocol/Makefile delete the line "include $(TOP)/configure/RULES.copy". Do this for <ioc name>App/srcProtocol/Makefile as well.
    # Create a file configure/RULES_BUILD with all the necessary info inside.
    app_srcProtocol_makefiles = []
    names = []
    file_app_srcProtocol_makefile1 = ""
    file_app_srcProtocol_makefile2 = ""

    parent = os.path.dirname(os.path.join(os.path.dirname(__file__), ""))
    grandparent = os.path.dirname(parent)
    greatgrandparent = os.path.dirname(grandparent)

    # Create lists of IOCs that have app/srcProtocol/Makefile and <ioc name>App/srcProtocol/Makefile
    # Delete the line "include $(TOP)/configure/RULES.copy" from each of these files
    for item in os.listdir(greatgrandparent):
        if os.path.isdir(os.path.join(greatgrandparent, item)) and "__" not in item:
            file_app_srcProtocol_makefile1 = greatgrandparent + \
                "/" + item + "/app/srcProtocol/Makefile"

            if os.path.exists(file_app_srcProtocol_makefile1):
                app_srcProtocol_makefiles.append(
                    file_app_srcProtocol_makefile1)

            name = item.split("-")
            ioc_name = ""

            try:
                name[3]
                ioc_name = name[2]
                for word in name[3:]:
                    ioc_name += "-" + word
                names.append(ioc_name)
                file_app_srcProtocol_makefile2 = greatgrandparent + "/" + \
                    item + "/" + ioc_name + "App/srcProtocol/Makefile"
                if os.path.exists(file_app_srcProtocol_makefile2):
                    app_srcProtocol_makefiles.append(
                        file_app_srcProtocol_makefile2)
            except IndexError:
                pass

            try:
                names.append(name[2])
                file_app_srcProtocol_makefile2 = greatgrandparent + "/" + \
                    item + "/" + name[2] + "App/srcProtocol/Makefile"
                if os.path.exists(file_app_srcProtocol_makefile2):
                    app_srcProtocol_makefiles.append(
                        file_app_srcProtocol_makefile2)
            except IndexError:
                pass

    for filepath in app_srcProtocol_makefiles:
        if os.path.isfile(filepath):
            with open(filepath, "r+") as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = line.replace("\t", "").strip()
                    newline = "".join(newline.split(" "))

                    if "RULES.copy" in newline and not line.startswith("#"):
                        newline = ""
                        newdata.append(newline.strip())

                    else:
                        newdata.append(line.strip())

            with open(filepath, "w") as outfile:
                for line in newdata:
                    outfile.write(line + "\n")

    # Create a file configure/RULES_BUILD with all the necessary info inside
    config_folders = []
    config_folder = ""

    parent = os.path.dirname(os.path.join(os.path.dirname(__file__), ""))
    grandparent = os.path.dirname(parent)
    greatgrandparent = os.path.dirname(grandparent)

    # Create lists of IOCs that have configure/RELEASE, configure/RELEASE.local
    # and RELEASE_SITE files
    for item in os.listdir(greatgrandparent):
        if os.path.isdir(os.path.join(greatgrandparent, item)) and "__" not in item:
            config_folder = greatgrandparent + "/" + item + "/configure"

            if os.path.exists(config_folder):
                config_folders.append(config_folder)

    # Go into all configure/ folders and check if there is a RULES_BUILD file. If not, create one.
    newdata = ['# RULES_BUILD', 'include $(EPICS_BASE)/configure/RULES_BUILD']

    for dir in config_folders:
        if os.path.exists(dir):
            filepath = dir + "/RULES_BUILD"
            if not os.path.exists(filepath):
                with open(filepath, "w") as outfile:
                    for line in newdata:
                        outfile.write(line + "\n")
                print(f"File 'RULES_BUILD' created in '{dir}'.")
            else:
                print(f"File 'RULES_BUILD' already exists in '{dir}'.")


def update_iocBoot_templates_Makefile():
    # In iocBoot/templates/Makefile, replace the line starting with "ARCH" with "ARCH = $$IF(ARCH,$$ARCH,rhel7-x86_64)" and
    # delete all instances of "-include $(TOP)/configure/RULES_BUILD"
    iocboot_templates_makefiles = []
    makefile = ""

    parent = os.path.dirname(os.path.join(os.path.dirname(__file__), ""))
    grandparent = os.path.dirname(parent)
    greatgrandparent = os.path.dirname(grandparent)

    # Create lists of IOCs that have app/src/Makefile files
    for item in os.listdir(greatgrandparent):
        if os.path.isdir(os.path.join(greatgrandparent, item)) and "__" not in item:
            makefile = greatgrandparent + "/" + item + "/iocBoot/templates/Makefile"

            if os.path.exists(makefile):
                iocboot_templates_makefiles.append(makefile)

    for filepath in iocboot_templates_makefiles:
        if os.path.isfile(filepath):
            print(filepath)
            with open(filepath, "r+") as file:
                data = file.readlines()
                newdata = []

                for line in data:
                    newline = line.replace("\t", "").strip()
                    newline = "".join(newline.split(" "))

                    if ("ARCH =" in newline or "ARCH=" in newline) and not line.startswith("#"):
                        newline = "ARCH = $$IF(ARCH,$$ARCH,rhel7-x86_64)"
                        newdata.append(newline.strip())

                    elif "RULES.copy" in newline and not line.startswith("#"):
                        newline = line.replace("RULES.copy", "RULES_BUILD")
                        newdata.append(newline.strip())

                    else:
                        newdata.append(line.strip())

            with open(filepath, "w") as outfile:
                for line in newdata:
                    outfile.write(line + "\n")


def main():
    replace_autosavedbd()
    replace_RULEScopy()
    update_iocBoot_templates_Makefile()


main()
