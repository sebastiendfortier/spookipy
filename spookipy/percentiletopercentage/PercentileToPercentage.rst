Description:
============

-  Calculate probability of exceedance of a threshold using ensemble percentiles.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-Point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 fields 

Result(s):
~~~~~~~~~~

-  A field with the result of the operation

Algorithm:
~~~~~~~~~~

.. code-block:: text

        Each percentile field y has a corresponding field of values x.

        At each point of the grid, a linear piece-wise function f is built such that f(x) = y.

        Then a threshold T is applied:

        For values lesser than the threshold (option le), the probability of exceeding the threshold is f(T).
        For values greater than the threshold (option ge), the probability of exceeding the threshold is 1 - f(T).

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, pourcentage/percentage, centile/percentile

Usage:
~~~~~~
   Note: With x being the percentile, the data frame should have
   an etiekt format of Cx followed by the rest of the conventional 
   etiket name. 

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/PercentileToPercentage/testsFiles/inputFile.std').to_pandas()
   df_field = df.loc[(df.typvar == selected_tv) & (df.nomvar == selected_nv) & (df.etiket.str.startswith('C'))]

   df_percentage = spooki.PercentileToPercentage(df_field,   
                                        threshold=0.3, 
                                        operator='ge', 
                                        etiket='GE0_____PALL',
                                        nomvar='SSH', 
                                        typvar='P@', 
                                        percentile_step='0,100,5').compute()

Contacts:
~~~~~~~~~
- Author : Benoit Pouliot
- Coded by : Logan Yu 
- Support: `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__