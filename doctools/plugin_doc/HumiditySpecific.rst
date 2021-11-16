========================
Spooki: HumiditySpecific
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

`HumiditySpecific <classHumiditySpecific.html>`__

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

`Français <../../spooki_french_doc/html/pluginHumiditySpecific.html>`__

**Description:**

-  Calculation of the specific humidity, the ratio of the mass of water
   vapour in the air to the total mass of moist air.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Water vapour mixing ratio, QV
   or
-  Air temperature, TT
   **and** one of the following fields:
-  Dew point temperature, TD / Dew point depression, ES
-  Humidité relative, HR

**Result(s):**

-  Specific humidity, HU (kg/kg)

**Algorithm:**

.. code-block:: text

            -If the --RPN key is NOT activated:

              *If the input field is the water vapour mixing ratio, QV (kg/kg)
                   HU = QV / (QV + 1)
                 where the specific humidity, HU is in kg/kg


              *If the input fields are the relative humidity, HR (fraction) or the dew point temperature, TD (deg C) / dew point depression, ES (deg K or deg C) and the air temperature, TT (deg C)
                 Calculation of the vapour pressure, VPPR (Pa) with the VapourPressure plug-in
                 Calculation of the pressure, PX (Pa) with the Pressure plug-in
                    HU = epsilon * ( VPPR / (PX - (1-epsilon)*VPPR))
                 where specific humidity, HU is in kg/kg and epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


            -If the --RPN key is activated:

              *If the input field is the water vapour mixing ratio, QV (kg/kg)
                 There is no RPN function for this calculation, therefore we use:
                   HU = QV / (QV + 1)
                 where the specific humidity, HU is in kg/kg

              *If the input fields are the relative humidity, HR (fraction) and the air temperature, TT (deg K)
                 Calculate the pressure, PX (Pa) with the Pressure plug-in
                 Call the function shrahu.ftn90 to obtain the specific humidity, HU (kg/kg)

              *If the input fields are the dew point temperature, TD (deg K) / the dew point depression, ES (deg K or deg C) and the air temperature, TT (deg K)
                 Calculate the dew point depression, ES (deg K or deg C) with the DewPointDepression plug-in if necessary
                 Calculate the pressure, PX (Pa) with the Pressure plug-in
                 Call the function sesahu.ftn90 to obtain the specific humidity, HU (kg/kg)


    Notes:  - When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with QV followed by HR and finally ES/TD.
            - When the TT field is not available, the calculation will be done with QV.
            - When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the sesahu.ftn90 and shrahu.ftn90 functions.

**Reference:**

-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipedia : Specific
   humidity <http://en.wikipedia.org/wiki/Specific_humidity>`__

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

**Usage:**

**Call example:** ````

::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumiditySpecific/testsFiles/inputFile.std] >>
                        [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
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

Reference to `HumiditySpecific <classHumiditySpecific.html>`__
:sup:``[code] <HumiditySpecific_8cpp_source.html>`__`

Units tests

`Evaluation tree <HumiditySpecific_graph.png>`__

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
