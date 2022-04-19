#!/usr/bin/env python

import argparse
import datetime
import json
import os
import subprocess
import tarfile
import yaml

mendatory_plugins = [
    "configparsingutils",
    "humidityutils",
    "opelementsbycolumn",
    "opelementsbyvalue",
    "plugin",
    "pressure",
    "science"
]
mendatory_files = [
    "__init__.py",
    "utils.py"
]

def main():
    parsed_arg = get_arguments()
    dir_livraison = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(dir_livraison)
    version = get_version(root_dir)
    plat = "all"
    name = "spookipy"

    pkg_name = "_".join([name,version,plat] if parsed_arg["suffix"] == "" else [name,version,plat,parsed_arg["suffix"]])

    # generate package file hierarchy
    temp_dir = dir_livraison+"/temp"
    os.mkdir(temp_dir)
    ssm = tarfile.open(name=pkg_name+".ssm",mode="w:gz")
    ssm.add(temp_dir,arcname=pkg_name+"/.ssm.d")
    ssm.add(temp_dir,arcname=pkg_name+"/bin")
    ssm.add(temp_dir,arcname=pkg_name+"/share")
    ssm.add(temp_dir,arcname=pkg_name+"/etc/profile.d")
    os.rmdir(temp_dir)

    # add requirements
    ssm.add(root_dir+"/ssm/requirements.txt",arcname=pkg_name+"/share/requirements.txt")

    # add setup script
    ssm.add(root_dir+"/ssm/ssm_package_setup.sh",arcname=pkg_name+"/etc/profile.d/"+pkg_name+".sh")

    # add control
    json_file = "control.json"
    generate_control_json(json_file, name, version, plat)
    ssm.add(json_file,arcname=pkg_name+"/.ssm.d/control.json")
    os.remove(json_file)

    # read yaml or generate list of all plugins
    if parsed_arg["yaml"]:
        with open(parsed_arg["yaml"], "r") as stream:
            try:
                plugin_list = yaml.safe_load(stream)
                plugin_list = plugin_list["plugins"]
            except yaml.YAMLError as exc:
                print(exc)
                raise("Could not read yaml file")

        plugins = plugin_list + mendatory_plugins
    
    else:
        plugins = get_all_plugins(root_dir)

    # add plugins to ssm package
    for plugin in plugins+mendatory_files:
        print(plugin)
        ssm.add(root_dir+"/"+name+"/"+plugin,arcname=pkg_name+"/lib/python/"+name+"/"+plugin)
    
    # generate and add all.py to package
    plugins.sort()
    all_file = "all.py"
    generate_all(all_file,plugins,pkg_name)
    ssm.add(all_file,arcname=pkg_name+"/lib/python/"+name+"/"+all_file)
    os.remove(all_file)

    # add Version
    ssm.add(root_dir+"/spookipy/VERSION",arcname=pkg_name+"/lib/python/"+name+"/VERSION")

    # close package
    ssm.close()

    if parsed_arg["install"]:
        install(pkg_name, dir_livraison, parsed_arg["temp"], name, version)

def get_version(root_dir):
    version_file = open(root_dir+"/VERSION","r")
    version = version_file.readline().strip()
    version_file.close()
    return version

def generate_control_json(file_name, name, version, plat):
    control = {
        "name": name,
        "version": version,
        "platform": plat,
        "maintainer": "CMDW",
        "description": "spookipy package",
        "x-build-date": datetime.datetime.now().strftime("%c"),
        "x-build-platform": os.getenv("BASE_ARCH"),
        "x-build-host": subprocess.run(["hostname","-f"], capture_output=True).stdout[0:-1].decode("utf-8"),
        "x-build-user": os.getenv("USER"),
        "x-build-uname": [
            subprocess.run(["uname","-s"], capture_output=True).stdout[0:-1].decode("utf-8"), 
            subprocess.run(["uname","-n"], capture_output=True).stdout[0:-1].decode("utf-8"),
            subprocess.run(["uname","-r"], capture_output=True).stdout[0:-1].decode("utf-8"),
            subprocess.run(["uname","-v"], capture_output=True).stdout[0:-1].decode("utf-8"),
            subprocess.run(["uname","-m"], capture_output=True).stdout[0:-1].decode("utf-8"),
        ]
    }

    # Serializing json 
    json_object = json.dumps(control, indent = 4)

    # Writing to control.json
    with open(file_name, "w") as outfile:
        outfile.write(json_object)

def generate_all(all_file, plugins,pkg_name):
    with open(all_file, "w") as outfile:
        outfile.write("# -*- coding: utf-8 -*-\n")

        for plugin in plugins:
            outfile.write("from ."+plugin+" import *\n")

        outfile.write("\nfrom .utils import *\n")

def get_arguments():

    description = "Makes the ssm package for spookipy with a YAML file."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--yaml", type=str, default="", help="YAML file with the list of plugins, if left empty it generate the package with all the plugin.")
    parser.add_argument("--suffix", type=str, default="", help="Suffix to add to the package name (ex: beta or operation).")
    parser.add_argument("--install", action="store_true", help="Do a local install.")
    parser.add_argument("--temp", type=str, help="Temporary path to install the package if the --install option is used.")
    return vars(parser.parse_args())

def install(pkg_name, dir_livraison, path, name, version):
    temp_path = path if path else dir_livraison
    process = subprocess.run(["ssm", "created", "-d", os.path.join(temp_path,"master")])
    process = subprocess.run(["ssm", "install", "-f", dir_livraison+"/"+pkg_name+".ssm", "-d", os.path.join(temp_path,"master")])

    try:
        os.mkdir(os.path.join(temp_path, name))
    except FileExistsError:
        print(name + " dir already exists")

    process = subprocess.run(["ssm", "created", "-d", os.path.join(temp_path,name,version)])

    process = subprocess.run(["ssm", "publish", "-d", os.path.join(temp_path,"master"), "-p", pkg_name, "-P", os.path.join(temp_path,name,version), "-pp", "all"])


def get_all_plugins(root_dir):

    plugins = []

    for file in os.listdir(root_dir+"/spookipy"):
        d = os.path.join(root_dir,"spookipy", file)
        if os.path.isdir(d):
            plugins.append(os.path.basename(d))
    return plugins


if __name__ == "__main__":
    main()
