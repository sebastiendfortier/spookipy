#!/usr/bin/env python

import argparse
import os
import subprocess
import yaml
from make_ssm_package import get_all_plugins, mendatory_plugins

dir_livraison = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(dir_livraison)

description = "Generate commands to run test from a yaml list of plugin"
parser = argparse.ArgumentParser(description=description)
parser.add_argument("--yaml", type=str, default="", help="YAML file with the list of plugins, if left empty it generate the package with all the plugin.")

yaml_file = parser.parse_args().yaml

print(yaml_file)

# read yaml or generate list of all plugins
if yaml_file:
    with open(yaml_file, "r") as stream:
        try:
            plugins = yaml.safe_load(stream)
            plugins = plugins["plugins"] + mendatory_plugins
            # print(x)
        except yaml.YAMLError as exc:
            print(exc)
            raise("Could not read yaml file")

else:
    plugins = get_all_plugins(root_dir)

plugins.sort()

for plugin in plugins:
    test_file = root_dir+"/test/"+plugin+"_test.py"
    print(test_file)

    if os.path.exists(test_file):
        process = subprocess.run(["pytest", "-v", test_file])
        # print(process.args)
        # print(process.returncode)
        # print(process.stdout)
    else:
        print("No test for this one")