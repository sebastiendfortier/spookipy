========================
Spooki: HumidityRelative
========================

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

`HumidityRelative <classHumidityRelative.html>`__

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

`Français <../../spooki_french_doc/html/pluginHumidityRelative.html>`__

**Description:**

-  Calculation of the relative humidity, the ratio between the partial
   pressure of water vapour content in the air and the saturated vapour
   pressure at the same temperature.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Air temperature, TT
   **and** one of the following fields:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD / Dew point depression, ES

**Result(s):**

-  Relative humidity, HR (fraction)

**Algorithm:**

.. code-block:: text

        -If the --RPN key is NOT activated:

            For the ambient temperature, TT (deg C):
                Calculation of the saturation vapour pressure, SVP (hPa) with the SaturationVapourPressure plug-in

            *If the input field is the specific humidity, HU (kg/kg) or
                the water vapour mixing ratio, QV (kg/kg) or
                the dew point temperature, TD (deg C) or
                the dew point depression, ES (deg K or deg C):

                Calculation of the vapour pressure, VPPR (hPa) with the VapourPressure plug-in
                HR = VPPR/SVP
                where HR is the relative humidity in fraction

        -If the --RPN key is activated:

            *If the input fields are the specific humidity, HU (kg/kg) and the air temperature, TT (deg K)
                Calculate the pressure, PX (Pa) with the Pressure plug-in
                Call the function shuahr.ftn90 to obtain the relative humidity, HR (fraction)

            *If the input fields are the water vapour mixing ratio, QV (kg/kg) and the air temperature, TT (deg K)
                Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in
                Calculate the pressure, PX (Pa) with the Pressure plug-in
                Call the function shuahr.ftn90 to obtain the relative humidity, HR (fraction)

            *If the input fields are the dew point temperature, TD (deg K) or
                the dew point depression, ES (deg K or deg C) and
                the air temperature, TT (deg K):

                Calculate the dew point depression, ES (deg K or deg C) with the DewPointDepression plug-in if necessary
                Calculate the pressure, PX (Pa) with the Pressure plug-in
                Call the function sesahr.ftn90 to obtain the relative humidity, HR (fraction)

    Note:  When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by QV and finally ES/TD.
           When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the sesahr.ftn90 and shuahr.ftn90 functions.

**Reference:**

-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipedia : relative
   humidity <http://en.wikipedia.org/wiki/Relative_humidity>`__

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumidityRelative/testsFiles/inputFile.std] >>
                    [HumidityRelative --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Daniel Figueras </wiki/Daniel_Figueras>`__
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__, `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `HumidityRelative <classHumidityRelative.html>`__
:sup:``[code] <HumidityRelative_8cpp_source.html>`__`

Units tests

`Evaluation tree <HumidityRelative_graph.png>`__

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
