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

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std').to_pandas()

   class MultiplyElementsByError(Exception):
      pass
      
   def mult_value(a, v):
      return a * v

   res_df = spookipy.OpElementsByValue(df,
                                 value=(1/3),
                                 operation_name='MultiplyElementBy',
                                 nomvar_out='MV',
                                 operator=mult_value,
                                 exception_class=MultiplyElementsByError,
                                 etiket='MULEBY').compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

- Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
- Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
- Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

