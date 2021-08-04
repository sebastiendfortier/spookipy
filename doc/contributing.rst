.. raw:: org

   #+TITLE_:CONTRIBUTING

Creating the developpement environment
======================================

.. code:: bash

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

Getting the source code
=======================

.. code:: bash

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

Then create a merge request on science's gitlab
https://gitlab.science.gc.ca/cmdw-spooki/spookipy/merge_requests

Testing
=======

.. code:: bash

   # From the $project_root/test directory of the project
   . activate spookipy_dev    
   # get rmn python library      
   . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2    
   # get fstpy ssm package
   . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.4/ 
   python -m pytest  

Building documentation
======================

.. code:: bash

   # This will build documentation in docs/build and there you will find index.html 
   # make sure fstpy is in the PYTHONPATH
   make clean    
   make doc