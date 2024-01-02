=================================
Spooki: PrecipitationTypeDominant
=================================

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

`PrecipitationTypeDominant <classPrecipitationTypeDominant.html>`__

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

`Français <../../spooki_french_doc/html/pluginPrecipitationTypeDominant.html>`__

**Description:**

-  Finds the dominant type of precipitation by choosing the type with
   maximum accumulation. Two fields are created for each time interval
   defined by the input data. For a given interval, the PDM field gives
   the dominant type and sub-type of precipitation and the QDM field
   gives the corresponding accumulation.

   ***Note:*** : Use the
   `PrecipitationAmount <pluginPrecipitationAmount.html>`__ plug-in if
   the input data does not define every desired interval.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Mandatory if the –microphysics option has the value of MY2 or P3 or
   BOURGOUIN:

   -  RN, accumulation of rain.
   -  SN, accumulation of snow.
   -  FR, accumulation of freezing rain.
   -  PE, accumulation of ice pellets.

-  Mandatory if the –microphysics option has the value of MY2 or P3:

   -  RN1, accumulation of drizzle.
   -  FR1, accumulation of freezing drizzle.
   -  SN1, accumulation of ice crystals.
   -  SN3, accumulation of graupel.

-  Mandatory if the –microphysics option has the value of CUSTOM:

   -  All fields specified by the following options: –rain, –drizzle,
      –freezingRain, –freezingDrizzle, –snow, –graupel, –icePellets,
      –iceCrystal, –hail and –snowGrain.

**Results:**

-  PDM: Dominant precipitation type and subtype field (no units, between
   100 and 500, 2D) on each time interval.
-  QDM: Accumulation field corresponding to the dominant type of
   precipitation (2D field in meters).

**Algorithm:**

-  https://wiki.cmc.ec.gc.ca/w/images/b/b7/SPOOKI_-_Algorithme_PrecipitationTypeDominant.odt
   (french only)
-  https://wiki.cmc.ec.gc.ca/w/images/8/85/SPOOKI_-_Algorithme_PrecipitationTypeDominant.pdf
   (french only)

| ***Notes on the types of precipitation:*** :

-  Type: The first digit represents the precipitation type.

   -  1\_\_: Liquid
   -  2\_\_: Freezing
   -  3\_\_: Ice pellets
   -  4\_\_: Solid
   -  5\_\_: No précipitation

-  Subtype of precipitation: The last two digits are in accordance with
   table
   `Table4-201 <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table4-201.shtml>`__.
   Les codes respectifs pour chaque sous-type sont donc:

   -  101: Rain
   -  111: Drizzle
   -  110: Hail
   -  203: Freezing rain
   -  212: Freezing drizzle
   -  308: Ice pellets
   -  409: Graupel (snow pellets)
   -  414: Snow grains
   -  405: Snow
   -  413: Ice crystals

**Reference:**

-  Does not apply

**Keywords:**

-  MÉTÉO/WEATHER, précipitations/precipitation, type, dominant,
   accumulation

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationTypeDominant/testsFiles/inputFile.std] >>
                    [TimeIntervalDifference --fieldName RN,SN,FR,PE --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >>
                    [PrecipitationTypeDominant --microphysics BOURGOUIN] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...
        

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`PrecipitationTypeDominant <classPrecipitationTypeDominant.html>`__
:sup:``[code] <PrecipitationTypeDominant_8cpp_source.html>`__`

Unit tests

`Evaluation tree <PrecipitationTypeDominant_graph.png>`__

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
