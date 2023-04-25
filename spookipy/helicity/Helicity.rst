Description:
~~~~~~~~~~~~

- Calculation of the relative helicity, necessary tool for the
   forecast of severe thunderstorms

Iteration method:
~~~~~~~~~~~~~~~~~

- Integration on a vertical air column (1D)

Dependencies:
~~~~~~~~~~~~~

- Zonal wind component UU (m / s) (relative to the north)
- Southern Wind component VV (m / s) (relative to the north)
- Wind component UV (m / s)
- Wind direction WD (deg)
- The geopotential height GZ (Km)

Result(s):
~~~~~~~~~~

- HL: Relative helicity (m2 / s2)

Algorithm:
~~~~~~~~~~

- `Helicity Algorithm <https://wiki.cmc.ec.gc.ca/images/8/82/Spooki_-_Algorithme_Helicity.pdf>`__

References:
~~~~~~~~~~~

- `Reference article <https://wiki.cmc.ec.gc.ca/images/c/c3/Spooki_-_Helicity_Characteristics.pdf>`__
- `Demonstration <https://wiki.cmc.ec.gc.ca/images/1/18/Spooki_-_Helicity.pdf>`__

Keywords:
~~~~~~~~~

- MÉTÉO/WEATHER, sévère/severe, été/summer, aviation, tornade/tornado, énergie/energy, éolienne

Usage:
~~~~~~

.. code:: python

    import os
    import fstpy
    import spookipy

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Helicity/testsFiles/inputFile.std')
    output_file = (f'{tmpdir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()

    res_df = spookipy.Helicity(df).compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

- Author: `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
- Coded by: `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
- Support: `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginHelicity.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginHelicity.html>`_
