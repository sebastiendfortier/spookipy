======================
Spooki: VapourPressure
======================

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

`VapourPressure <classVapourPressure.html>`__

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

`Francais <../../spooki_french_doc/html/pluginVapourPressure.html>`__

**Description:**

-  Calculates the vapour pressure of water.
   ***Note:*** If calculating from HR or ES/TD the user has to define if
   these were calculated with respect to water saturation or ice
   saturation

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Specific Humidity, HU
   or
-  Water vapour mixing ratio, QV
   or
-  Air Temperature, TT
   **and** one of the following fields:
-  Relative Humidity, HR
-  Dew point temperature, TD / Dew point depression, ES

**Result(s):**

-  Vapour pressure, VPPR (hPa)

**Algorithm:**

.. code:: fragment

        -If the --RPN key is NOT activated:

            *If the input field is the specific humidity, HU (kg/kg):
                Calculate the atmospheric pressure, PX (hPa) with the Pressure plug-in.
                VPPR= (HU*PX) / ( epsilon + HU*(1-epsilon) )
                where the vapour pressure, VPPR is in hPa and epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


            *If the input field is the water vapour mixing ratio, QV (kg/kg)
                Calculate the atmospheric pressure, PX (hPa) with the Pressure plug-in.
                VPPR= (QV*PX) / (epsilon + QV)
                where the vapour pressure, VPPR is in hPa and epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


            *If the input fields are the relative humidity, HR (fraction) and the air temperature, TT (deg C)
                Calculate the saturation vapour pressure, SVP (hPa) by using the SaturationVapourPressure plug-in.
                VPPR = HR*SVP
                where the vapour pressure, VPPR is in hPa.


            *If the input fields are the dew point depression, ES (deg C or deg K)/ dew point temperature, TD (deg C) and the air temperature, TT (deg C)
                For TPL, the temperature at which we must change from the saturation with respect to water to the saturation with respect to ice (deg C)
                Calculate the dew point temperature, TD (deg C), with the TemperatureDewPoint plug-in.

                If TT>TPL or --iceWaterPhase WATER
                    VPPR = AEw1 * exp( (AEw2*TD)/(AEw3 + TD) )
                else
                    VPPR = AEi1 * exp( (AEi2*TD)/(AEi3 + TD) )

                where the vapour pressure, VPPR is in hPa and where according to Alduchov and Eskridge (1996)
                AEw1=6.1094   AEi1=6.1121
                AEw2=17.625   AEi2=22.587
                AEw3=243.04   AEi3=273.86


        -If the --RPN key is activated:

            *If the input field is the specific humidity, HU (kg/kg)
                Calculate the pressure, PX (Pa) with the Pressure plug-in
                Call the rpn function sfoefq.ftn90 to obtain the vapour pressure, VPPR (Pa)

            *If the input field is the water vapour mixing ratio, QV (kg/kg)
                Calculate the pressure, PX (hPa) with the Pressure plug-in.
                There is no RPN function for this calculation, we therefore use:
                VPPR= (QV*PX) / (epsilon + QV)
                where the vapour pressure, VPPR is in hPa and epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.

            *If the input fields are the relative humidity HR (fraction) and the air temperature, TT (deg K)
                Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in (with the same keys and their arguments)
                Calculate the pressure, PX (hPa) with the Pressure plug-in.
                Call the rpn function sfoefq.ftn90 to obtain the vapour pressure, VPPR (Pa)

            *If the input fields are the dew point depression, ES (deg K or deg C)/ dew point temperature, TD (deg K) and the air temperature (deg K)
                For TPL, the temperature at which we must change from the saturation with respect to water to the saturation with respect to ice (deg K)
                Calculate the dew point temperature, TD (deg K), with the TemperatureDewPoint plug-in.

                If TT >TPL or --iceWaterPhase Water
                    Call the rpn function sfoewa.ftn90 with TD to obtain the vapour pressure, VPPR (Pa)
                else
                    Call the rpn fucntion sfoew.ftn90 with TD to obtain the vapour pressure, VPPR (Pa)


        Convert the vapour pressure, VPPR to hPa if VPPR is in Pa
            VPPR(hPa)= VPPR(Pa) / 100.0


    Notes: When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by QV, HR and finally ES/TD.
           When the TT field is not available, the calculation will be done in order of preference with HU followed by QV disregarding the number of levels.

**Reference:**

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.
-  `Alduchov, O. A., and R. E. Eskridge, 1996: Improved Magnus form
   approximation of saturation vapor pressure. ''J. Appl. Meteor.'',
   '''35''',
   601-609 <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__
-  `Analyse de la pression de
   vapeur <https://wiki.cmc.ec.gc.ca/wiki/RPT/Analyse_de_la_pression_de_vapeur>`__
-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

**Keywords:**

-  MÉTÉO/WEATHER, humidité/humidity, pression/pressure

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VapourPressure/testsFiles/inputFile.std] >>
                    [VapourPressure] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `VapourPressure <classVapourPressure.html>`__
:sup:``[code] <VapourPressure_8cpp_source.html>`__`

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
