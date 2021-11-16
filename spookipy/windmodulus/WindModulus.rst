Description:
============

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

#. Call example:

.. code:: python

        python3

        import os
        import fstpy.all as fstpy
        import spookipy.all as spooki

        spooki_dir = os.environ['SPOOKI_DIR']

        user = os.environ['USER']

        df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std').to_pandas()

        res_df = spooki.WindModulus(df).compute()

        fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginWindModulus.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginWindModulus.html>`_
