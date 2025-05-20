Description:
~~~~~~~~~~~~

-  Simple calculator plugin that performs arithmetic operations on input fields and returns the result.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  One or more fields

Result(s):
~~~~~~~~~~

-  A field with the result of the calculation

Algorithm:
~~~~~~~~~~

-  Before calculation, fields are grouped by `grid`, `dateo` and `datev`. If all rows of the DataFrame contain ensemble members,
   an additional grouping by `ensemble_member` will be done. Within each group, only commons levels are kept.
   The expression is then evaluated for each point in the input fields, and the results are stored in a new output field.

Reference:
~~~~~~~~~~

- `NumExpr: Fast numerical expression evaluator for NumPy <https://github.com/pydata/numexpr>`__

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, calculatrice/calculator

Usage:
~~~~~~

.. code:: python
   
   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Calculator/testsFiles/2020061900_024_glbpres')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file, query='nomvar in ["UU", "VV"]').to_pandas()

   res_df = spookipy.Calculator(df, 'sqrt(UU**2+VV**2)', nomvar_out='UV', unit='knot').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginCalculator.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginCalculator.html>`_
