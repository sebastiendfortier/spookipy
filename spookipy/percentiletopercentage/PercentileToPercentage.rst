Description:
~~~~~~~~~~~~

-  Calculates the probability of exceedance of a threshold using ensemble percentiles.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-Point

Dependencies:
~~~~~~~~~~~~~

-  Percentile fields

Result(s):
~~~~~~~~~~

-  The probability of exceedance from input

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

   With x being the percentile, the data frame records should have
   an etiket format containing 'x' followed by the rest of the conventional 
   etiket name. 

.. code:: python

   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/PercentileToPercentage/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   source_df = src_df0.loc[(src_df0['etiket'].str.contains('C') ) &
                           (src_df0['nomvar'] == 'SSH')]

   res_df = spookipy.PercentileToPercentage(source_df, 
                                            threshold=0.7, 
                                            operator='le',
                                            label='STG1LE').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()
                                     

Contacts:
~~~~~~~~~
- Author   : Benoit Pouliot
- Coded by : Logan Yu 
- Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
