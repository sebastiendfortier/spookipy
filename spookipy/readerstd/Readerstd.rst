Description:
~~~~~~~~~~~~

- Reading of standard file(s) and conversion into the system's internal memory structure.
- The information associated to the spacial representation (also called "meta-information"), is read automatically and is conserved by default throughout the calculations.
- The variable dictionary is consulted during the reading of each variable and its corresponding unit is associated by default.
- Note: if two identical records are present in the input file, only the first will be kept

Iteration method:
~~~~~~~~~~~~~~~~~

- Does not apply

Dependencies:
~~~~~~~~~~~~~

- One or more valid standard file(s) Note: The forecast hour is extracted with the help of the record descriptors DEET and NPAS and not directly from the record descriptor IP2

Result(s):
~~~~~~~~~~
- Standard files received from input converted into internal memory structure

Algorithm:
~~~~~~~~~~
- Does not apply
 

Reference:
~~~~~~~~~~

- `Documentation on standard files <https://wiki.cmc.ec.gc.ca/w/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
- `Correspondence between the standard file descriptors of the records and the attributes of the internal memory of SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI>`__ 


Keywords:
~~~~~~~~~

- IO, lecteur/reader, décodeur/decoder, standard , fichier/file

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

      
      df = spookipy.ReaderStd(df=pd.DataFrame,
                            input=input_file).compute()

      fstpy.StandardFileWriter(output_file, df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Farooq Chaudhary <https://wiki.cmc.ec.gc.ca/wiki/User:Chaudharyf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__, `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginReaderStd.html>`_

`English <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginReaderStd.html>`_