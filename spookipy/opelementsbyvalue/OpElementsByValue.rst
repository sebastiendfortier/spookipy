Description:
~~~~~~~~~~~~

-  Generic plugin used by other plugins to apply specific operations with a value as parameter on a point of data

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-Point

Dependencies:
~~~~~~~~~~~~~

-  At least 1 field

Result(s):
~~~~~~~~~~

-  A field with the result of the operation

Algorithm:
~~~~~~~~~~

-  Does not apply

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, generique/generic, point

Usage:
~~~~~~

.. code:: python

   import os
   import fstpy
   import spookipy

   class MultiplyElementsByError(Exception):
      pass

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   def mult_value(a, v):
      return a * v

   res_df = spookipy.OpElementsByValue(df,
                                 value=(1/3),
                                 operation_name='MultiplyElementBy',
                                 nomvar_out='MV',
                                 operator=mult_value,
                                 exception_class=MultiplyElementsByError,
                                 label='MULEBY').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()


Contacts:
~~~~~~~~~

- Author   : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
- Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
- Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

