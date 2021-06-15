SPOOKIPY


# Introduction

## What is it?

spookipy is a collection of python weather algorithms to work with
dataframes obtained with fstpy or numpy arrays.

## Spookipy philosophy

These algorithms are generic in nature and all share a uniform model in
implementation. The idea is to use the interface to create new
algorithms.

# Requirements

## packages

-   python 3.6
-   numpy
-   pandas
-   fstpy


## Using spookipy in scripts or Jupyter Lab/Notebook

``` {.bash org-language="sh"}
# activate your conda environment     
. activate spooki_pwa_req     
# get rmn python library      
. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2      
# get spookipy ssm package
. ssmuse-sh -d /fs/site4/eccc/cmd/w/sbf000/spookipy-beta-0.0.0      
# get fstpy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.2/      
```

### use spookipy

``` {.python}
# inside your script    
import spookipy.all as spookipy   
uv_df = spookipy.windmodulus(df).compute()
```

### Example

``` {.python}
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


CONTRIBUTING

# Contributing

## Creating the developpement environment

``` {.bash org-language="sh"}
# get conda if you don't already have it  
. ssmuse-sh -x cmd/cmdm/satellite/master_u1/miniconda3_4.9.2_ubuntu-18.04-skylake-64   
# create a conda environment for spookipy's requirements   
conda create -n spooki_pwa_dev python=3.6   
# whenever you need to use this environment on science run the following (if you have'nt loaded the conda ssm, you'll need to do it everytime)
# unless you put it in your profile
. activate spooki_pwa_dev   
# installing required packages in spooki_pwa_req environment  
conda install sphinx
conda install -c conda-forge sphinx-autodoc-typehints
conda install -c conda-forge sphinx-gallery
conda install -c conda-forge sphinx_rtd_theme
conda install numpy pandas dask xarray pytest
# for a full jupyter developpement environment (spooki_pwa_dev.yaml is located in project root)
conda env create -f spooki_pwa_dev.yaml
```

## Getting the source code

``` {.bash org-language="sh"}
git clone git@gitlab.science.gc.ca:sbf000/spookipy.git
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
<https://gitlab.science.gc.ca/sbf000/spookipy/merge_requests>

## Testing

``` {.bash org-language="sh"}
# From the $project_root/test directory of the project
. activate spooki_pwa_dev    
# get rmn python library      
. r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2    
# get fstpy ssm package
. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.2/ 
python -m pytest  
```

## Building documentation

``` {.bash org-language="sh"}
# This will build documentation in docs/build and there you will find index.html 
make clean    
make doc
```

CMC CONDA HOWTO

# Conda basics

\[<https://kiwidamien.github.io/save-the-environment-with-conda-and-how-to-let-others-run-your-programs.html>\]\[conda
reference\]\]

## get cmc conda

``` {.bash org-language="sh"}
. ssmuse-sh -x cmd/cmdm/satellite/master_u1/miniconda3_4.9.2_ubuntu-18.04-skylake-64
```

## create an environment

``` {.bash org-language="sh"}
conda create --name spookipy python=3.6
```

## activate an environment

``` {.bash org-language="sh"}
. activate spookipy
```

## install stuff in the env

``` {.bash org-language="sh"}
conda install -c conda-forge sphinx-autodoc-typehints
conda install -c conda-forge sphinx-gallery
conda install -c conda-forge sphinx_rtd_theme
conda install ipykernel
conda install jupyterlab
conda install numpy pandas dask xarray pytest
conda install sphinx
```

## export env to file

``` {.bash org-language="sh"}
conda env exportspooki_pwa.yaml
```

## deactivate the env

``` {.bash org-language="sh"}
conda deactivate
```

## deleting the env

``` {.bash org-language="sh"}
conda env remove --name spookipy
```

## list all envs

``` {.bash org-language="sh"}
conda info --envs
```

## recreate the env from yml specs

``` {.bash org-language="sh"}
conda env create --file spookipy.yaml
```
