Description:
~~~~~~~~~~~~

-  Apply a unary function the data, point by point

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field

Result(s):
~~~~~~~~~~

-  The meteorological field to which the unary function has been applied to each element

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For F, a field of n elements
         For Func, a unary function
         for each point
            F(n) = Func(F(n))


Reference:
~~~~~~~~~~

-  `numpy Math routines <https://numpy.org/doc/stable/reference/routines.math.html>`__

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, unaire/unary

Usage:
~~~~~~

.. code:: python

    import numpy as np
    import os
    import fstpy
    import spookipy

    spooki_dir     = os.environ['SPOOKI_DIR']
    spooki_out_dir = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/AddToElement/testsFiles/inputFile.std')
    output_file = (f'{spooki_out_dir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()


    res_df = spookipy.ApplyUnary(df,
                                function=np.sqrt,
                                nomvar_in='UU*',
                                nomvar_out='UUSQ',
                                etiket='SQRT'
                                ).compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()



Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

