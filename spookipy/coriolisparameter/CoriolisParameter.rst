Description:
~~~~~~~~~~~~

-  Calculation of the Coriolis parameter.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point by point

Dependencies:
~~~~~~~~~~~~~

-  A field on a grid known by SPOOKI.

Result(s):
~~~~~~~~~~

-  Coriolis parameter, CORP (1/s)

Algorithm:
~~~~~~~~~~

   For OMEGA = 7.2921 * 10^-5 (1/s) and varphi (radians),
   the latitude.
   Calculate the Coriolis parameter, CORP (1/s), with the
   following formula:
   CORP = 2 * OMEGA * sin( varphi)

Reference:
~~~~~~~~~~

-  "An Introduction to Dynamic Meteorology", Holton, James R.

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, Coriolis, paramètre/parameter


Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/CoriolisParameter/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.CoriolisParameter(df).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Simon Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Coded by : `Simon Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginCoriolisParameter.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginCoriolisParameter.html>`_
