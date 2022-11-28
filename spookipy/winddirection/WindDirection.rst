Description:
~~~~~~~~~~~~

- Calculation of the meteorological wind direction (where the vector is coming from with respect to north) from its 2 horizontal components.

Iteration method:
~~~~~~~~~~~~~~~~~

- Point-by-point

Dependencies:
~~~~~~~~~~~~~

- UU component of the wind (along the X axis of the grid). 
- VV component of the wind (along the Y axis of the grid).

Result(s):
~~~~~~~~~~

- Meteorological wind direction, WD, in degrees.

Algorithm:
~~~~~~~~~~

    For WD, the direction : If the direction is calculated with the
    meteorological convention (--orientationType WIND), then : the
    gduvfwd function of the EZSCINT library is used to calculate the
    direction of where the vector is coming from with respect to north

Reference:
~~~~~~~~~~

- Does not apply

Keywords:
~~~~~~~~~

- MÉTÉO/WEATHER, direction/direction, vent/wind, vitesse/speed

Usage:
~~~~~~

.. code:: python

    import os
    import fstpy
    import spookipy

    spooki_dir     = os.environ['SPOOKI_DIR']
    spooki_out_dir = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/WindDirection/testsFiles/inputFile.std')
    output_file = (f'{spooki_out_dir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()

    res_df = spookipy.WindDirection(df).compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

- Author   : `Maryse Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
- Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
- Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__,  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
