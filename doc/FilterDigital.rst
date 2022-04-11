Description:
~~~~~~~~~~~~

-  Apply a digital filter of Stencil type on a data set.
-  The filter, applied on one given point, in one direction of the
   given field, is characterized by a list of weights (odd number)
   symmetrical to the considered point and to the number of times
   it is applied.
-  The filter is applied successively in each direction of the
   given field.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A meteorological field on a grid.

Result(s):
~~~~~~~~~~

-  The filtered values of the meteorological field.

Algorithm:
~~~~~~~~~~

   For F, a given field of components F(i), in the direction NI
   (i=1,NI).


   For :math:`w_n, (n=1,N)` a list of N weights associated to the digital filter applied on the F field, which the result
   :math:`F^*` on each component is expressed as :

   :math:`F^*(i) = \frac{\sum_{n=1}^{N} w_n F(i - {\scriptstyle[\frac{N+1}{2}- n]})} {\sum_{n=1}^{N} w_n}, 2 \leq i \leq NI-1`

   This operation is repeated ("repetitions" key), in the
   direction NI, as many times as the specified number in
   parameter.

   We proceed in the same way in each direction of the F field,
   successively.

   Note: : in the case of a 2D field, the algorithm is first
   applied in the direction NI, and then in the direction NJ.


Reference:
~~~~~~~~~~

-  `Inspired from the FILTRE function (stenfilt.f) of the PGSM utility <https://wiki.cmc.ec.gc.ca/images/d/dc/Spooki_-_Filtre_html.pdf>`__

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, filtre/filter, digital, stencil

Usage:
~~~~~~



.. code:: python

   python3
   
   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/FilterDigital/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.FilterDigital(df, filter=[1,2,1], repetitions=2).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginFilterDigital.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginFilterDigital.html>`_
