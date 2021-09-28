==============================
Spooki: WaterVapourMixingRatio
==============================

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

`WaterVapourMixingRatio <classWaterVapourMixingRatio.html>`__

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

`Francais <../../spooki_french_doc/html/pluginWaterVapourMixingRatio.html>`__

**Description:**

-  Calculates the water vapour mixing ratio, which is the ratio of the
   mass of water vapour to the mass of dry air.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Specific humidity, HU or
-  Air temperature, TT and one of the following fields:
-  Relative humidity, HR
-  Dewpoint temperature, TD / Dewpoint depression, ES

NOTE: Make sure to provide the dependencies listed above to this plug-in
or to the plug-in results called by this plug-in (see the section "this
plug-in uses"). For more details on this alternative use, see the
`documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
page.

**Result(s):**

-  Water vapour mixing ratio, QV (g kg-1)

**Algorithm:**

.. code:: fragment

        -If the --RPN key is NOT activated:

            *If the input field is specific humidity, HU (kg/kg):
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.


            *If the input fields are relative humidity, HR (fraction) or
                dew point temperature, TD (deg C)/ dew point depression, ES (deg K or deg C) and
                the air temperature, TT (deg C):

                Calculate the vapour pressure, VPPR (Pa) with the VapourPressure plug-in.
                Calculate the pressure, PX (Pa) with the Pressure plug-in.
                QV = epsilon * [VPPR/(PX-VPPR)]
                where QV is the water vapour mixing ratio in kg/kg and
                epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


        -If the --RPN key is activated:

            *If the input field is specific humidity, HU (kg/kg):
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.

            *If the input fields are relative humidity, HR (fraction) or
                dew point temperature, TD (deg C)/ dew point depression, ES (deg K or deg C) and
                the air temperature, TT (deg C):

                Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in (with the same keys as their arguments)
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.


        Convert QV in g/kg:
            QV(g/kg) = QV(kg/kg)*1000.0


    Notes: When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by HR and finally ES/TD.
           When the TT field is not available, the calculation will be done in order of preference with HU.
           When the --RPN key is activate and the attribute to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the sesahu.ftn90 and shrahu.ftn90 functions which are called by the HumiditySpecific plug-in.

**Reference:**

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.
-  `Analysis of water vapour mixing
   ratio <https://wiki.cmc.ec.gc.ca/wiki/RPT/en/Analysis_of_water_vapour_mixing_ratio>`__
-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf%20>`__

**Keywords:**

-  WEATHER/METEO, humidity/humidite, ratio/rapport, pressure/pression

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WaterVapourMixingRatio/testsFiles/inputFile.std] >>
                    [WaterVapourMixingRatio] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`WaterVapourMixingRatio <classWaterVapourMixingRatio.html>`__
:sup:``[code] <WaterVapourMixingRatio_8cpp_source.html>`__`

Units tests

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
