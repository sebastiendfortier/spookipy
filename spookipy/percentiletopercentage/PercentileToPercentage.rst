Description:
~~~~~~~~~~~~

-  Calculate probability of exceedance of a threshold using ensemble percentiles.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-Point

Dependencies:
~~~~~~~~~~~~~

-  One standard file that contains percentile fields

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

.. note::

   With x being the percentile, the data frame should have
   an etiekt format of Cx followed by the rest of the conventional 
   etiket name. 

.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/PercentileToPercentage/testsFiles/inputFile.std').to_pandas()

   df_percentage = spookipy.PercentileToPercentage(df_field,   
                                        threshold=0.3, 
                                        operator='ge', 
                                        etiket='GESTG1PALL',
                                        nomvar='SSH', 
                                        typvar='P@').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', df_percentage).to_fst()                                        

Contacts:
~~~~~~~~~
- Author : Benoit Pouliot
- Coded by : Logan Yu 
- Support: `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
