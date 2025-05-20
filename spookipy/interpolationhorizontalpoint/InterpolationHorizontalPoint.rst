Description:
~~~~~~~~~~~~

- Horizontal interpolation of one or more field (s) on a set of points of given latitudes and longitudes.
- The fields can be scalar (ex: temperature) or vectorial (e.g. horizontal wind).
   Note:: Only the wind can be vector interpolated.

Iteration method:
~~~~~~~~~~~~~~~~~

- Point by point

Dependencies:
~~~~~~~~~~~~~

- One or more field(s) on one or more grid(s) source(s)
- A destination field of latitudes (LAT), in decimal degrees signed
- A destination field of longitudes (LON), in decimal degrees signed

Result(s):
~~~~~~~~~~

- One or more field(s) interpolated over a number of given latitudes and longitudes points

Algorithm:
~~~~~~~~~~

- Detects the scalar or vector nature of the fields entered on the source grid  
- Calls the scalar or vector routines of the library EZSCINT according to the nature of the fields and configurable keys  
- Returns the interpolated fields at points, latitudes and given longitudes  

References:
~~~~~~~~~~~

- `EZSCINT Library RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

Keywords:
~~~~~~~~~

-  INTERPOLATION, extrapolation, horizontale/horizontal, point, ezscint

Usage:
~~~~~~

.. code:: python
    
    import os
    import numpy as np
    import pandas as pd
    import fstpy
    import spookipy

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.std')
    output_file = (f'{tmpdir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()

    # build lat lon dataframe
    base = {'shape': (1,1),  'dateo': 0,  'datev': 0, 'path': None, 'typvar': 'X', 'ni': 1, 
            'nj': 1, 'nk': 1, 'ip1': 0, 'ip2': 0, 'ip3': 0, 'deet': 0, 'npas': 0, 
            'datyp': 5, 'nbits': 32, 'grtyp': 'L', 'ig1': 100, 'ig2': 100, 'ig3': 9000, 'ig4': 0}
    lat = base.copy()
    lat['nomvar'] = 'LAT'
    lon = base.copy()
    lon['nomvar'] = 'LON'

    lat['d']  = np.expand_dims(np.array([45.73, 43.40, 49.18], dtype=np.float32), axis=-1)
    lat['ni'] = lat['d'].shape[0]
    lat['nj'] = lat['d'].shape[1]
    lon['d']  = np.expand_dims( np.array([-73.75, -79.38, -123.18], dtype=np.float32), axis=-1)
    lon['ni'] = lon['d'].shape[0]
    lon['nj'] = lon['d'].shape[1]
    latlon    = [lat, lon]
    latlon_df =  pd.DataFrame(latlon)

    df_and_lat_lon = pd.safe_concat([df, latlon_df])

    res_df = spookipy.InterpolationHorizontalPoint(
        df_and_lat_lon,
        interpolation_type='bi-linear',
        extrapolation_type='value',
        extrapolation_value=99.9).compute()


    fstpy.StandardFileWriter(output_file, res_df).to_fst()


-  `Other examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Examples_of_horizontal_interpolation_to_a_set_of_latitude.2Flongitude_points>`__

Contacts:
~~~~~~~~~

-  Auteur(e) : `Sandrine Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginInterpolationHorizontalPoint.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginInterpolationHorizontalPoint.html>`_
