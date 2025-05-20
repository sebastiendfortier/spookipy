Description:
~~~~~~~~~~~~

- Select one or more field(s) in the internal memory structure, depending on one or more argument(s) passed to the parameter keys.
- NOTE: in the case of field(s) extracted from standard files, all the meta-information is automatically selected with all selection of field(s) (unless if one of the optional --noMetadata or --metadataFieldName parameter keys is specified)


Iteration method:
~~~~~~~~~~~~~~~~~

- Does not apply

Dependencies:
~~~~~~~~~~~~~

- At least one field in the internal memory structure

Result(s):
~~~~~~~~~~
- One or more selected field(s) depending on the arguments passed to the parameter keys

Algorithm:
~~~~~~~~~~
- Index, with the help of a dataframe, the records depending on the selection criteria
- Select with the help of the appropriate index(es)
- Return the result
 

Reference:
~~~~~~~~~~

- `Components of the internal memory structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_syst%C3%A8me#meteo_infos>`__
- `Correspondence between the standard file descriptors of the records and the attributes of the internal memory of SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI>`__ 


Keywords:
~~~~~~~~~

- SYSTÈME/SYSTEM, sélection/select

Usage:
~~~~~~

.. code:: python

      import os
      import fstpy
      import spookipy
      
      spooki_dir  = os.environ['SPOOKI_DIR']
      tmpdir      = os.environ['BIG_TMPDIR']

      input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Select/testsFiles/input_big_fileSrc.std')
      output_file = (f'{tmpdir}/outputFile.std')

      src_df0 = fstpy.StandardFileReader(input_file).to_pandas()

      res_df = spookipy.Select(
                src_df0, 
                nomvar=['TT'],
                vertical_level=[1.0],
                label=['928V4'],
                reduce_df=False).compute()

      fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Farooq Chaudhary <https://wiki.cmc.ec.gc.ca/wiki/User:Chaudharyf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__, `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/Select.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/Select.html>`_