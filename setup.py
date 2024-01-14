# -*- coding: utf-8 -*-
import setuptools
from numpy.distutils.core import setup, Extension

ext_module = Extension(
   name='fstpy/filterdigital/f_stenfilt',
   sources=['fstpy/filterdigital/f_stenfilt.f90'],
   extra_compile_args=['-g','--backtrace'],
   extra_link_args=[],
   f2py_options=['--debug-capi'],
   language='f90'
)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


v_file = open("VERSION")
__version__ = v_file.readline()
v_file.close()

setuptools.setup(
    name="spookipy",  # Replace with your own username
    version=__version__,
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
        'pandas>=1.2.4', 'fstpy>=2023.11.0','xarray>=0.19.0','numpy>=1.19.5','dask>=2021.8.0'
    ],
    packages=setuptools.find_packages(exclude='test'),
    include_package_data=True,
    python_requires='>=3.6',
    ext_modules=[ext_module]
)
