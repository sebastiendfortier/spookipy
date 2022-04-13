Description:
~~~~~~~~~~~~

-  Calculation of value differences of a given field for each grid point. 
-  The difference can be calculated in three different ways on each axis of the grid :

   -  centered distance : for one given point, difference of the value of the field between the previous point and the next point
   -  forward distance : for one given point, difference of the value of the field between this point and the next point
   -  backward distance : for one given point, difference of the value of the field between this point and the previous point

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A field on a grid or at least on one of the calculation axis (X,Y,Z)

Result(s):
~~~~~~~~~~

-  Central, forward or backward difference(s) of a field for each grid point.

Algorithm:
~~~~~~~~~~

.. code-block:: text

   For F a given field and N its dimension along a given axis X ("axis" key)
   For n (n=1, N), the point from where we want to calculate the central, forward or backward difference of the field F.
   The calculation along the X axis results in :
            If differenceType = CENTERED then
               F(1) = F(2) - F(1)
               F(n) = F(n+1) - F(n-1) for 2 <= n <= N-1
               F(N) = F(N) - F(N-1)
            Else if differenceType = FORWARD then
               F(N) = F(N) - F(N-1)
               F(n) = F(n+1) - F(n) for 1 <= n <= N-1
            Else if differenceType = BACKWARD then
               F(1) = F(2) - F(1)
               F(n) = F(n) - F(n-1) for 2 <= n <= N
            Endif


.. note::

   For forward or backward differences, the calculated differences will repeat at one of the boundaries in order to conserve a coherent data structure.

Reference:
~~~~~~~~~~

-  "Numerical Recipes: The Art of Scientific Computing" par W.H. Press, B.P. Flannery, S.A. Teukolsky et W.T. Vetterling

Customizable condition:
~~~~~~~~~~~~~~~~~~~~~~~

-  N/A

Keywords:
~~~~~~~~~

-  grille/grid, point, difference, centrée/centered, arrière/backward, avant/forward

Usage:
~~~~~~

.. code:: python

    python3
    
    import os
    import fstpy.all as fstpy
    import spookipy.all as spooki

    spooki_dir = os.environ['SPOOKI_DIR']

    user = os.environ['USER']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/GridPointDifference/testsFiles/inputFile.std').to_pandas()

    res_df = spooki.GridPointDifference(df, axis=['x','y'], difference_type='centered').compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginGridPointDifference.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginGridPointDifference.html>`_
