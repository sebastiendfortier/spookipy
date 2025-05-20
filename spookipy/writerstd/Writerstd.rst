Description:
~~~~~~~~~~~~

- Writing data into a file in RPN standard format
- Convert, by default, each variable to the unity corresponding to the standard variables dictionary.

Iteration method:
~~~~~~~~~~~~~~~~~

- Does not apply

Dependencies:
~~~~~~~~~~~~~

- Data in the internal memory of the SPOOKI system (PDS)

Result(s):
~~~~~~~~~~
- One or more encoded record(s) in a file of RPN standard format
- The records are sorted and written in the following order : meta-informations, names of the variables in alphabetic order, level order (from bottom to top), temporal order

Algorithm:
~~~~~~~~~~
- With the help of the table on the correspondence between `the standard file and SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI>`__ , this plug-in transfers (writes) the information of the attributes from the internal memory of SPOOKI to the record descriptors of the standard files by following theses rules.
- Convert each variable to its standard unit designated by `the standard variables dictionary <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/stdvar.html>`__, with the help of the `UnitConvert <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/classUnitConvert.html>`__ plug-in, unless the "--noUnitConversion" key is activated. During this conversion, the second character of TYPVAR is not affected. If the original unit is unknown, the conversion cannot be done, the plug-in stops by indicating: "The unit is unknown, if you wish to write the variable with the original unit, use the &ndash;noUnitConversion key."
- Sort the variables in the order designated by the system (meta-informations, names of the variables in alphabetic order, level order (from bottom to top), temporal order).
- If the "--noMetadata" key is activated, do not copy the "meta-informations" (information associated to the spacial representation: ">>","^^","HY","P0","P0LS","PT","E1","!!","!!SF" records).
- If the "--metadataOnly" key is activated, only copy the "meta-informations" (information associated to the spacial representation: ">>","^^","HY","P0","P0LS","PT","E1","!!","!!SF" records).
- This plug-in writes to the file named by the argument given to the "--output" key. If this file already exists, by default (APPENDOVERWRITE option of the "--writingMode" key), we write over the records that have the same values in the record descriptors as the new data and we keep the other data that is already in the file. If we choose the NOPREVIOUS option of the "--writingMode" key and the file already exists, the plug-in stops with an appropriate message. If we chose the NEWFILEONLY option, we erase the file and we create a new file containing exclusively the new data. Important: If the file (in the –output argument) already exists and this file is not a standard file, the request stops by indicating that the file in the –output argument already exists and is not of standard type. We then invite the user to resolve the conflict before relaunching SPOOKI.
- The final file does not contain two distinct fields of "HY" or of "!!". For the "^^" and ">>", the distinct fields are allowed unless they have the same IP1 and IP2 but not the same IG1,IG2,IG3 and IG4. If a second distinct "HY" or "!!" or disallowed distinct "^^" and ">>" fields exist in the data to be written and/or in the writing file, the request stops with a clear message explaining the problem.
 

Reference:
~~~~~~~~~~

- `Documentation on standard files <https://wiki.cmc.ec.gc.ca/w/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
- `Table of comparison between the standard file and SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI>`__ 


Keywords:
~~~~~~~~~

- IO, standard, graveur/writer, fichier/file

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

      src_df = fstpy.StandardFileReader(input_file).to_pandas()

      spookipy.WriterStd(df, results_file).compute()



Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__, `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__, `Luc Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
-  Coded by : `Audrey Germain <https://wiki.cmc.ec.gc.ca/wiki/Audrey_Germain>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__, `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginWriterStd.html>`_

`English <https://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginWriterStd.html>`_