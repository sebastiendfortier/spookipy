Description:
~~~~~~~~~~~~

-  Arithmetic mean for each point of all the fields received

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 different fields

Result(s):
~~~~~~~~~~

-  The mean of the fields received from input named "MEAN"

Algorithm:
~~~~~~~~~~

.. code-block:: text

    For N fields Fn , (n=1,N)

    The arithmetic mean of the N fields received from input is
    expressed for each point (i,j,k) as :

    mean(i, j) = sum(i, j, 0..N)/N

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, moyenne/mean, average

Usage:
~~~~~~



.. code:: python

    python3
    
    import os
    import fstpy
    import spookipy

    spooki_dir = os.environ['SPOOKI_DIR']

    user = os.environ['USER']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/ArithmeticMeanByPoint/testsFiles/inputFile.std').to_pandas()

    res_df = spookipy.ArithmeticMeanByPoint(df).compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginArithmeticMeanByPoint.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginArithmeticMeanByPoint.html>`_
