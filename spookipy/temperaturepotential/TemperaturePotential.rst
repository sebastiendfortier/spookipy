Description:
============

-  Calculate probability of exceedance of a threshold using ensemble percentiles.

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
         It is a piece-wise linear interpolation from the percentiles into a risk likelyhood percentage

         For the operator variable le/ge

         When 0th percentile is greater than threshold value, likelyhood is 0 | 100 
         If 100th percentile is less than threshold value, likelyhood is 100 | 0 
         If threshold matches exactly a x th percentile, likelyhood is x | 100 - x
         If threshold matches exactly multiple percentiles, likely hood is (highest percentile - lowest percentile / 2) | 100 - (highest percentile - lowest percentile / 2)
         If threshold is between two x, y percentiles, likely hood can be calculated with x 

Reference:
~~~~~~~~~~

-

Keywords:
~~~~~~~~~

-  

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

   res_df = spooki.PercentileToPercentage(df).compute()

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