Description:
============

- Horizontal interpolation of one or more field (s) on a target grid  
- The target grid can be either defined by the user, according to the parameters given in option, or correspond to the grid of one of the fields given as input  
- The fields can be scalar (ex: temperature) or vector (ex: horizontal wind)  

   Notes:

   - Only the wind can be vector interpolated  
   - Only processes the grids which are defined as in the standard files  
   - Interpolation on Y or Z type grids, defined by the user, not available for the moment  

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point by point

Dependencies:
~~~~~~~~~~~~~

- One or more field (s) on one or more grid(s) source(s)
- With the option –outputGridDefinitionMethod FIELD_DEFINED: One field on a target grid whose name is different from(s) field(s) on the source grid(s)

Result(s):
~~~~~~~~~~

- One or more interpolated field (s) on a target grid

Algorithm:
~~~~~~~~~~

- Detects the scalar or vector nature of the field entered on the source grid
- Calls the scalar or vector routines of the EZSCINT library according to the nature of the fields and configurable keys, appropriate to the target grid
- Returns the interpolated field on the target grid

References:
~~~~~~~~~~~

-  `Documentation on the differtent types of supported grids <http://web-mrb.cmc.ec.gc.ca/science/si/eng/si/misc/grilles.html>`__
-  `EZSCINT Library RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

Keywords:
~~~~~~~~~

-  INTERPOLATION, extrapolation, horizontale/horizontal, grille/grid, ezscint

Usage:
~~~~~~



.. code:: python

    python3
    
    import os
    import fstpy.all as fstpy
    import spookipy.all as spooki

    spooki_dir = os.environ['SPOOKI_DIR']

    user = os.environ['USER']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/InterpolationHorizontalGrid/testsFiles/inputFile.std').to_pandas()

    res_df = spooki.InterpolationHorizontalGrid(
        df=df
        method='user',
        grtyp='N',
        ni=191,
        nj=141,
        param1=79.0,
        param2=117.0,
        param3=57150.0,
        param4=21.0,
        interpolation_type='bi-linear',
        extrapolation_type='value',
        extrapolation_value=99.9).compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

-  `Other examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Example_of_horizontal_interpolation>`__


Contacts:

-  Auteur(e) : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Codé par : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginInterpolationHorizontalGrid.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginInterpolationHorizontalGrid.html>`_