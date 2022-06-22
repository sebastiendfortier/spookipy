# Introduction

## What is it?

Spookipy is a collection of python algorithms that work with dataframes
obtained with fstpy or numpy arrays.

## Spookipy philosophy

These algorithms are generic in nature and all share a uniform model in
implementation. The idea is to use the interface to create new
algorithms.

# Requirements

## run time packages

-   fstpy>=2.1.10
-   pandas>=1.2.4
-   numpy>=1.19.5
-   xarray>=0.19.0
-   dask>=2021.8.0

## developpement packages

-   fstpy>=2.1.10
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
-   nbsphinx>=0.8.7

## Surgepy

This is an ssm package that we use at CMC on the science network and
that contains a wide variety of packages

``` bash
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
```

# Installation

Use the ssm package

    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/1.0.1

## Using spookipy in scripts or Jupyter Lab/Notebook

``` bash
# load surgepy
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
# get spookipy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/1.0.1/
```

### use spookipy

``` python
# inside your script
import spookipy
uv_df = spookipy.windmodulus(df).compute()
```

### Example

``` python
data_path = prefix + '/data/'
import fstpy.all as fstpy
import spookipy
# setup your file to read
records=fstpy.StandardFileReader(data_path + 'ttuvre.std').to_pandas()
# display selected records in a rpn voir format
fstpy.voir(records)
# compute uv on the selected records
uv_df = spookipy.windmodulus(records).compute()
dest_path = '/tmp/out.std'
# write the selected records to the output file
fstpy.StandardFileWriter(dest_path,uv_df).to_fst()
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
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
# get fstpy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.10/
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

The plugin_list.txt in \$project_root will be used to determine which
plugins to put in the ssm package.

``` bash
# This will build the ssm package
# From the $project_root/ssm directory of the project
./make_ssm_package.sh
```
