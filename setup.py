# -*- coding: utf-8 -*-
import setuptools
import subprocess
import shutil
import sys
from pathlib import Path
import re


def get_package_version():
    init_py = Path(__file__).resolve().parent / "spookipy" / "__init__.py"
    version_regex = r"__version__\s*=\s*['\"]([^'\"]*)['\"]"
    try:
        with open(init_py, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(version_regex, content)
            if match:
                return match.group(1)
            else:
                print("Warning: __version__ not found in __init__.py")
                return "unknown"
    except Exception as e:
        print(f"Error reading version from __init__.py: {e}")
        return "unknown"


def run_make():
    subprocess.check_call(["make", "-C", "spookipy/filterdigital", "all"])


def check_dependency(executable):
    if shutil.which(executable) is None:
        print(f"ERROR: {executable} is not installed.")
        sys.exit(1)


check_dependency("f2py")
check_dependency("make")

run_make()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="spookipy",  # Replace with your own username
    version=get_package_version(),
    author="Sebastien Fortier",
    author_email="sebastien.fortier@canada.ca",
    description="spooki's weather algorithms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.science.gc.ca/cmds/spookipy",
    project_urls={
        "Bug Tracker": "https://gitlab.science.gc.ca/CMDS/spookipy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Linux",
    ],
    install_requires=[
        "pandas>=1.2.4",
        "fstpy>=2024.08.00",
        "xarray>=0.19.0",
        "numpy>=1.19.5",
        "dask>=2021.8.0",
    ],
    packages=setuptools.find_packages(exclude="test"),
    include_package_data=True,
    python_requires=">=3.6",
    package_data={
        "spookipy": ["filterdigital/*.so*", "filterdigital/*.pyf"],
    },
)
