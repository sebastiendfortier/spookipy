.. raw:: org

   #+TITLE_: USAGE

Using spookipy in scripts or Jupyter Lab/Notebook
=================================================

.. code:: bash

   # activate your conda environment     
   . activate spookipy_req     
   # get rmn python library      
   . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2      
   # get spookipy ssm package
   . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/0.0.0/      
   # get fstpy ssm package
   . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/fstpy/2.1.3/      

use spookipy
------------

.. code:: python

   # inside your script    
   import spookipy.all as spookipy   
   uv_df = spookipy.windmodulus(df).compute()

Example
-------

.. code:: python

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
