# Introduction

## What is it?

spookipy is a collection of python weather algorithms to work with
dataframes obtained with fstpy or numpy arrays.

## spookipy philosophy

These algorithms are generic in nature and all share a uniform model in
implementation. The idea is to use the interface to create new
algorithms.

# Requirements

## run time packages

-   fstpy>=2.1.8
-   pandas>=1.2.4
-   numpy>=1.19.5
-   xarray>=0.19.0
-   dask>=2021.8.0

## developpement packages

-   fstpy>=2.1.8
-   ci_fstcomp>=1.0.2
-   pandas>=1.2.4
-   numpy>=1.19.5
-   xarray>=0.19.0
-   dask>=2021.8.0
-   pytest>=5.3.5
-   Sphinx>=3.4.3
-   sphinx-autodoc-typehints>=1.12.0
-   sphinx-gallery>=0.9.0
-   sphinx-rtd-theme>=1.0.0

# Installation

Use the ssm package

    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/1.0.0

## Using spookipy in scripts or Jupyter Lab/Notebook

``` bash
# activate your conda environment
. activate spookipy_req
# get rmn python library
. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
# get spookipy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/1.0.0/
# get fstpy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/fstpy/2.1.6/
```

### use spookipy

``` python
# inside your script
import spookipy.all as spookipy
uv_df = spookipy.windmodulus(df).compute()
```

### Example

``` python
data_path = prefix + '/data/'
import fstpy.all as fstpy
import spookipy.all as spooki
# setup your file to read
records=fstpy.StandardFileReader(data_path + 'ttuvre.std').to_pandas()
# display selected records in a rpn voir format
fstpy.voir(records)
# compute uv on the selected records
uv_df = spooki.windmodulus(records).compute()
dest_path = '/tmp/out.std'
# write the selected records to the output file
fstpy.StandardFileWriter(dest_path,uv_df).to_fst()
```

## Creating the developpement environment

``` bash
# get conda if you don't already have it
. ssmuse-sh -x cmd/cmdm/satellite/master_u1/miniconda3_4.9.2_ubuntu-18.04-skylake-64
# create a conda environment for spookipy's requirements
conda create -n spookipy_dev python=3.6
# whenever you need to use this environment on science run the following (if you have'nt loaded the conda ssm, you'll need to do it everytime)
# unless you put it in your profile
. activate spookipy_dev
# installing required packages in spookipy_req environment
conda install sphinx
conda install -c conda-forge sphinx-autodoc-typehints
conda install -c conda-forge sphinx-gallery
conda install -c conda-forge sphinx_rtd_theme
conda install numpy pandas dask xarray pytest
```

## Getting the source code

``` bash
git clone git@gitlab.science.gc.ca:cmdw-spooki/spookipy.git
# create a new branch
git checkout -b my_change
# modify the code
# commit your changes
# fetch changes
git fetch
# merge recent master
git merge origin master
# push your changes
git push origin my_change
```

Then create a merge request on science\'s gitlab
<https://gitlab.science.gc.ca/cmdw-spooki/spookipy/merge_requests>

## Testing

``` bash
# From the $project_root/test directory of the project
. activate spookipy_dev
# get rmn python library
. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
# get fstpy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.6/
python -m pytest
```

## Building documentation

``` bash
# This will build documentation in docs/build and there you will find index.html
# make sure fstpy is in the PYTHONPATH
# From the $project_root/doc directory of the project
make clean
make doc
```

# Creating the ssm package

``` bash
# This will build the ssm package
# From the $project_root/ssm directory of the project
./make_ssm_package.sh
```
