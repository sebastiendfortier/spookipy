Description:
============

-  Calculation of a temporal difference of fields at various given intervals.
-  The various intervals are defined by the parameter keys.
-  This plug-in can be used, for example, for the calculation of precipitation accumulations.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Temporal difference, point-by-point

Dependencies:
~~~~~~~~~~~~~

-  The fields at every hour required for the desired calculations.

Result(s):
~~~~~~~~~~

-  Temporal difference of fields at each interval, with the same
   units as the dependencies.

Algorithm:
~~~~~~~~~~

.. code-block:: text

         1) Create a complete list of the time interval pairs desired:

            Where:
            N is the number of temporal intervals in --rangeForecastHour
            rangeStart(n) is the first value of the nth temporal interval in --rangeForecastHour
            rangeEnd(n) is the second value of the nth temporal interval in --rangeForecastHour
            interval(n) is the nth value in --interval
            step(n) is the nth value in --step
            k is the total number of desired calculations

            k = 0
            For n = 1,N

            k = k + 1
            startime(k) = rangeStart(n)
            endtime(k)  = 0.0

            Loop while ( startime(k) + interval(n) ) <=rangeEnd(n)
               endtime(k) = startime(k) + interval(n)
               If endtime(k) < rangeEnd(n)
                  k = k + 1
                  startime(k) = startime(k-1) + step(n)
               End If
            End Loop

            n = n + 1
            End For

         2) For every field in --fieldName loop on every desired interval:

            Where:
            M is the number of fields in --fieldName
            VAR(m,x) is the mth field in --fieldName at the time x
            RVAR(m,y) is the difference value of the field VAR(m) between the two times
            k is the number of desired calculations such as calculated in part 1.

            For m = 1,M
            ii = 0
            For ii < k+1
               RVAR(m,ii) = VAR(m,endtime(ii)) - VAR(m,startime(ii))
               ii = ii + 1
            End For
            m = m + 1
            End For

Reference:
~~~~~~~~~~

-  Inspired from the operational script : "img.pcpn_intvl"

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, différence/difference, accumulation,
   temps/time, temporel/temporal, intervalle/interval

Usage:
~~~~~~

   Note: A single value from each list of the –interval and
   –step conditions applies to a single temporal interval defined
   in –rangeForecastHour. The order of the values in the lists of
   the –interval and –step conditions, must correspond to the
   order in the –rangeForecastHour list.

Usage:
~~~~~~



.. code:: python

   python3

   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki
   import datetime

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/TimeIntervalDifference/testsFiles/inputFile.std').to_pandas()

   range1 = (datetime.timedelta(hours=0),datetime.timedelta(hours=177))
   range2 = (datetime.timedelta(hours=0),datetime.timedelta(hours=160))
   interval1 = datetime.timedelta(hours=12)
   interval2 = datetime.timedelta(hours=3)
   step1 = datetime.timedelta(hours=24)
   step2 = datetime.timedelta(hours=6)

   res_df = spooki.TimeIntervalDifference(df, nomvar='PR', forecast_hour_range=[range1, range2], interval=[interval1, interval2], step=[step1, step2]).compute()

   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Sandrine Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginTimeIntervalDifference.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginTimeIntervalDifference.html>`_
