
Description:
~~~~~~~~~~~~

-   Allows to rename one or more value(s) of field attribute(s) in the internal memory structure of the system,
    without affecting the data itself.
    Note: the arguments given to the parameter keys correspond to the new values of the attributes


Iteration method:
~~~~~~~~~~~~~~~~~

-  Does not apply

Dependencies:
~~~~~~~~~~~~~

- At least one field in the internal memory structure

Result(s):
~~~~~~~~~~
- One or more field(s) which the attribute value(s) are renamed in accordance with the arguments given to the parameter keys

Algorithm:
~~~~~~~~~~

-  Does not apply

Reference:
~~~~~~~~~~

-  `Components of the internal memory structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components#meteo_infos:>`__
-  `Correspondence between the recording descriptors of standard files and the attributes of the internal memory of SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI>`__

Keywords:
~~~~~~~~~

-  SYSTME/SYSTEM, zap, renommer/rename

Usage:
~~~~~~

.. code:: python

      import os
      import fstpy
      import spookipy
      
      spooki_dir  = os.environ['SPOOKI_DIR']
      tmpdir      = os.environ['BIG_TMPDIR']

      input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Zap/testsFiles/inputFile.std')
      output_file = (f'{tmpdir}/outputFile.std')

      df = fstpy.StandardFileReader(input_file).to_pandas()

      res_df = spookipy.Zap(df).compute()

      fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `Philippe Théroux <https://wiki.cmc.ec.gc.ca/wiki/User:Therouxp>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__, `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginZap.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginZap.html>`_
