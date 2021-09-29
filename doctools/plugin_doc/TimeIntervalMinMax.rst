==========================
Spooki: TimeIntervalMinMax
==========================

.. raw:: html

   <div id="top">

.. raw:: html

   <div id="titlearea">

+--------------------------------------------------------------------------+
| .. raw:: html                                                            |
|                                                                          |
|    <div id="projectname">                                                |
|                                                                          |
| Spooki                                                                   |
|                                                                          |
| .. raw:: html                                                            |
|                                                                          |
|    </div>                                                                |
+--------------------------------------------------------------------------+

.. raw:: html

   </div>

.. raw:: html

   <div id="main-nav">

.. raw:: html

   </div>

.. raw:: html

   <div id="MSearchSelectWindow"
   onmouseover="return searchBox.OnSearchSelectShow()"
   onmouseout="return searchBox.OnSearchSelectHide()"
   onkeydown="return searchBox.OnSearchSelectKey(event)">

.. raw:: html

   </div>

.. raw:: html

   <div id="MSearchResultsWindow">

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="header">

.. raw:: html

   <div class="headertitle">

.. raw:: html

   <div class="title">

`TimeIntervalMinMax <classTimeIntervalMinMax.html>`__

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="contents">

.. raw:: html

   <div class="textblock">

`Francais <../../spooki_french_doc/html/pluginTimeIntervalMinMax.html>`__

**Description:**

-  Calculation of the minimum/maximum of a field whitin a specified time
   frame. The various intervals have to be defined through the parameter
   keys. This plugin can be use to calculated the maximal humidex value.

**Iteration method:**

-  Temporal difference, point-by-point

**Dependencies:**

-  At least 2 fields to make the desired calculations. It is the
   responsability of the user to make sure that all the desired fields
   to make the calculation are present. (This can be done using the
   select plugin). Spooki will use all the available fields between the
   begining and the end of the time interval.

**Result(s):**

-  Temporal maximum or minimum of a field whithin the specified time
   interval. The result has the same units as the input.

**Algorithm:**

.. code:: fragment

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

**Reference:**

-  Inspired from the operational script : "img.pcpn\_intvl"

**Keywords:**

-  UTILITAIRE/UTILITY, différence/difference, accumulation, temps/time,
   temporel/temporal, intervalle/interval

**Usage:**

    ***Note:*** A single value from each list of the –interval and –step
    conditions applies to a single temporal interval defined in
    –rangeForecastHour. The order of the values in the lists of the
    –interval and –step conditions, must correspond to the order in the
    –rangeForecastHour list.

**Call example:** ````

::

         ...
         spooki_run "[ReaderStd --ignoreExtended --input $SPOOKI_DIR/pluginsRelatedStuff/TimeIntervalMinMax/testsFiles/global20121217_fileSrc.std] >>
                     [TimeIntervalMinMax --fieldName PR --type MIN --rangeForecastHour 0@177,0@60 --interval 12,3 --step 24,6] >>
                     [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion --noMetadata --encodeIP2andIP3]"
         ...
     

**Results validation:**

**Contacts:**

-  Auteur(e) : `Agnieszka
   Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Codé par : `Philippe
   Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `TimeIntervalMinMax <classTimeIntervalMinMax.html>`__
:sup:``[code] <TimeIntervalMinMax_8cpp_source.html>`__`

`Unit tests <classTimeIntervalMinMax.html>`__

`Evaluation tree <TimeIntervalMinMax_graph.png>`__

| **Uses:**

| **Used by:**

.. raw:: html

   </div>

.. raw:: html

   </div>

--------------

Generated by  |doxygen| 1.8.13

.. |doxygen| image:: doxygen.png
   :class: footer
   :target: http://www.doxygen.org/index.html
