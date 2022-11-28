Description:
~~~~~~~~~~~~

-  Calculation of the wind modulus from its 2 horizontal components.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  UU component of the wind (along the X axis of the grid).
-  VV component of the wind (along the Y axis of the grid).

Result(s):
~~~~~~~~~~

-  Wind modulus, UV, in the same units as the dependencies.

Algorithm:
~~~~~~~~~~

-  Hypotenuse of UU and VV


Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, module/modulus, vent/wind, vitesse/speed

Usage:
~~~~~~

.. code:: python

        import os
        import fstpy
        import spookipy

        spooki_dir     = os.environ['SPOOKI_DIR']
        spooki_out_dir = os.environ['BIG_TMPDIR']

        input_file  = (f'{spooki_dir}/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std')
        output_file = (f'{spooki_out_dir}/outputFile.std')

        df = fstpy.StandardFileReader(input_file).to_pandas()

        res_df = spookipy.WindModulus(df).compute()

        fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginWindModulus.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginWindModulus.html>`_
