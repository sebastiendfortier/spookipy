
Description:
~~~~~~~~~~~~

-  Calculation of the maximum value of the wind modulus determined according to the vertical, 
   as well as the horizontal components of the wind and the corresponding pressure level.

Iteration method:
~~~~~~~~~~~~~~~~~

-  column-by-column

Dependencies:
~~~~~~~~~~~~~

- UU component of the wind
- VV component of the wind
- PX pressure field

Result(s):
~~~~~~~~~~
- Maximum wind modulus, UV (knots)
- UU component of the wind corresponding to the maximum wind modulus found (knots)
- VV component of the wind corresponding to the maximum wind modulus found (knots)
- Associated PX pressure level (mb)

Algorithm:
~~~~~~~~~~

-  `WindMax algorithm <https://wiki.cmc.ec.gc.ca/w/images/2/26/Spooki_-_Algorithme_WindMax.pdf>`__

Reference:
~~~~~~~~~~

-  N/A

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, vent/wind, maximum, vitesse/speed

Usage:
~~~~~~

.. code:: python

      import os
      import fstpy
      import spookipy
      
      spooki_dir  = os.environ['SPOOKI_DIR']
      tmpdir      = os.environ['BIG_TMPDIR']

      input_file  = (f'{spooki_dir}/pluginsRelatedStuff/WindMax/testsFiles/inputFile.std')
      output_file = (f'{tmpdir}/outputFile.std')

      df = fstpy.StandardFileReader(input_file).to_pandas()

      res_df = spookipy.WindMax(df).compute()

      fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__, `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginWindMax.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginWindMax.html>`_
