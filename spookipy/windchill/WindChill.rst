Description:
~~~~~~~~~~~~

-  Calculation of the equivalent temperature associated to the wind chill factor at the surface.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Air surface temperature, TT
-  UU wind component (along the X axis of the grid), at the surface
-  VV wind component (along the Y axis of the grid), at the surface

Note: Be sure to provide the dependencies mentioned above
      to this plug-in or the results of
      the plug-ins called by this plug-in (See the "this plug-in
      uses" section). For more details on this
      alternative use, see the
      `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
      page.

Result(s):
~~~~~~~~~~

-  Wind chill factor, RE (deg C)

Algorithm:
~~~~~~~~~~

    For TT(1), the surface temperature (deg C) and UV(1), the
    surface wind modulus (km.h-1) (respectively, at 2 meters and 10
    meters),
    the wind chill factor RE (no units) is calculated according to
    the Osczevski-Bluestein equation, as :

.. code-block:: text
    
    if TT(1) <= 0 et UV(1) >= 5 then :
        RE = 13.1200 + 0.6215*TT(1) + (0.3965*TT(1) - 11.3700)*UV(1)^0.16
    else
        RE = TT

Reference:
~~~~~~~~~~

-  `The new wind chill equivalent temperature chart. Osczevski, R. and Bluestein, M., Amer. Meteor. Soc., 2005 <http://journals.ametsoc.org/doi/abs/10.1175/BAMS-86-10-1453>`__
-  `Wikipédia : wind chill factor <http://en.wikipedia.org/wiki/Wind_chill>`__

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, vent/wind, facteuréolien/windchill, facteur/factor, refroidissement/chill

Usage:
~~~~~~

.. code:: python

    import os
    import fstpy
    import spookipy

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std').to_pandas()

    res_df = spookipy.WindChill(df).compute()

    fstpy.StandardFileWriter(f'{tmpdir}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author   : `Marc Besner <https://wiki.cmc.ec.gc.ca/wiki/User:Besnerm>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__ / `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginWindChill.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginWindChill.html>`_
