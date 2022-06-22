Description:
~~~~~~~~~~~~

-  Calculate precipitation accumulations for given time intervals.
-  The various time intervals are defined according to the parameterized conditions.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Precipitation accumulation fields required to calculate the requested time interval accumulations.
-  All precipitation accumulation types found in o.dict may be used:
-  
   Ex. PR, FR, PE, RN, SN, A[1-4], AE, AMX, ASG, ASH, ASN, FR[1|2], PB, PC, PE[1|2], PE2L, PM, PY, PZ, RN[1|2], SN[1-3], SN10, SND, SNLR, etc

Result(s):
~~~~~~~~~~

-  Precipitation accumulation fields (2D) for the requested time intervals, in the same units as the dependencies.

Algorithm:
~~~~~~~~~~

-  Call plug-in `TimeIntervalDifference <pluginTimeIntervalDifference.html>`__ with the values of the four parameter keys.
-  The -fieldName key may only be used with the fields listed in the Dependencies section.

Reference:
~~~~~~~~~~

-  Inspired by operational script "img.pcpn_intvl"

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, précipitations/precipitation, différence/difference, type, temps/time, intervalle/interval, accumulation

Usage:
~~~~~~

.. note::

   A single value from each list of the -interval and
   -step conditions applies to a single range defined by
   -rangeForecastHour. The order of the values in the lists of the
   -interval and -step conditions must correspond to the order in the -rangeForecastHour list.


.. code:: python

    python3
    
    import os
    import fstpy
    import spookipy
    import datetime

    spooki_dir = os.environ['SPOOKI_DIR']

    user = os.environ['USER']

    df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/PrecipitationAmount/testsFiles/inputFile.std').to_pandas()

    range = (datetime.timedelta(hours=0),datetime.timedelta(hours=48))
    interval = datetime.timedelta(hours=3)
    step = datetime.timedelta(hours=1)

    res_df = spookipy.PrecipitationAmount(df, nomvar='SN', forecast_hour_range=range, interval=interval, step=step).compute()

    fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()


Contacts:
~~~~~~~~~

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginPrecipitationAmount.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginPrecipitationAmount.html>`_
