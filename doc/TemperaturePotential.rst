Description:
~~~~~~~~~~~~

-  Calculates the potential temperature, which is the temperature
   of an air parcel following adiabatic expansion or compression
   to a reference pressure. On a tephigram such a process can be
   visualized by raising or lowering a parcel along a dry adiabat.
   Note: The reference pressure used here is 1000 hPa.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air temperature, TT
-  Pressure , PX

Result(s):
~~~~~~~~~~

-  Potential temperature, TH (deg K)

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For TT, the air temperature (deg K) and
         PX the air pressure (hPa)

         Calculate TH as:

         TH = TT*(1000/PX)**(Rd/cpd)

         Where Rd is the gas constant for dry air (Rd = 287.04 J/(kg*K)),
         and cpd is the specific heat of dry air (cpd = 1005.46 J/(kg*K))

Reference:
~~~~~~~~~~

-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology in Midlatitudes. Wiley-Blackwell, 407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics, 3rd Ed. Butterworth Heinemann, 290 pp.

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, température/temperature, potentielle/potential

Usage:
~~~~~~

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TemperaturePotential/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.TemperaturePotential(df).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : Neil Taylor
-  Coded by : Jonathan Cameron, `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginTemperaturePotential.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginTemperaturePotential.html>`_
