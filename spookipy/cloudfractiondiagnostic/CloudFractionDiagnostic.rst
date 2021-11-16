Description:
============

- At a given level, the program converts the values
  relative humidity (HR) as a diagnostic cloud fraction
  using a formula derived from the work of Slingo (1987). the
  calculation of the cloud fraction depends on HR and a value
  empirical threshold that can vary vertically.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point by point

Dependencies:
~~~~~~~~~~~~~

-  HR : Relative humidity (unitless, between 0 and 1).

Result(s):
~~~~~~~~~~~~

- The cloud fraction field diagnoses at each point of
  grid, field in 3D. Without unit, between 0 and 1. CLD

Algorithm:
~~~~~~~~~~

-  http://iweb.cmc.ec.gc.ca/~afsyyah/Algorithme_DiagnostiqueCloudFraction_v1.1.doc

Reference:
~~~~~~~~~~~

-  `Slingo_1987 <https://wiki.cmc.ec.gc.ca/images/6/6f/Spooki_-_Slingo_1987.pdf>`__
-  `McFarlane_et_al_1992 <https://wiki.cmc.ec.gc.ca/images/e/e6/Spooki_-_McFarlane_et_al_1992.pdf>`__

Keywords:
~~~~~~~~~~

-  MÉTÉO/WEATHER, fraction, nuageu/cloudy, nuage/cloud, diagnostique/diagnostic, slingo

Usage:
~~~~~~



.. code:: python

  python3

  import os
  import fstpy.all as fstpy
  import spookipy.all as spooki

  spooki_dir = os.environ['SPOOKI_DIR']

  user = os.environ['USER']

  df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/CloudFractionDiagnostic/testsFiles/inputFile.std').to_pandas()

  res_df = spooki.CloudFractionDiagnostic(df).compute()

  fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Auteur(e) : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginCloudFractionDiagnostic.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginCloudFractionDiagnostic.html>`_