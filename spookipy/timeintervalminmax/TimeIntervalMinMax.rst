Description:
~~~~~~~~~~~~

-  Calculation of the minimum/maximum of a field whitin a specified time frame. 
-  The various intervals have to be defined through the parameter keys. 
-  This plugin can be use to calculated the maximal humidex value.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Temporal difference, point-by-point

Dependencies:
~~~~~~~~~~~~~

-  At least 2 fields to make the desired calculations. It is the
   responsability of the user to make sure that all the desired
   fields to make the calculation are present. (This can be done
   using the select plugin). Spooki will use all the available
   fields between the begining and the end of the time interval.

Result(s):
~~~~~~~~~~

-  Temporal maximum or minimum of a field whithin the specified
   time interval. The result has the same units as the input.

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

      k=0
      # Boucler sur chaque ensemble d'instructions
      for n= 1,N
         startime(k) = rangeStart(n)
         endtime(k) = 0.
         # Loop while all the intervals must be calculated.
         While ( startime(k) + interval(n) ) <= rangeEnd(n)
            endtime(k) = startime(k) + interval(n)
            i = 0
            #Pour chaque intervalle, lire les champs nécessaires aux calculs, et prendre le min ou le max.
            # C'est-à-dire, lire les champs entre startime(k) et endtime(k). Prendre le maximum et ou minimum de ceux-ci.

               #Si tous les champs de l'intervalle ont été traités, on passe au prochain intervalle, et on détermine son heure de début
                  Si endtime(k) < rangeEnd(n)
                        k = k + 1
                        startime(k) = startime(k-1) + step(n)
                  fin si
            fin boucle
         fin boucle
         n = n + 1
      End for

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



.. code:: python

   import os
   import fstpy
   import spookipy
   import datetime
   
   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/TimeIntervalMinMax/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   range1    = (datetime.timedelta(hours=0),datetime.timedelta(hours=177))
   range2    = (datetime.timedelta(hours=0),datetime.timedelta(hours=160))
   interval1 = datetime.timedelta(hours=12)
   interval2 = datetime.timedelta(hours=3)
   step1     = datetime.timedelta(hours=24)
   step2     = datetime.timedelta(hours=6)
   
   res_df    = spookipy.TimeIntervalMinMax(df, 
                                           nomvar='PR', 
                                           min=True, 
                                           forecast_hour_range=[range1, range2], 
                                           interval=[interval1, interval2], 
                                           step=[step1, step2]).compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()
     
Contacts:
~~~~~~~~~

-  Auteur(e) : `Agnieszka Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Codé par  : `Philippe Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support   : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginTimeIntervalMinMax.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginTimeIntervalMinMax.html>`_
