==================
Spooki: SweatIndex
==================

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

`SweatIndex <classSweatIndex.html>`__

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

`Francais <../../spooki_french_doc/html/pluginSweatIndex.html>`__

**Description:**

-  Calculation of the SWEAT index (Severe Weather Threat Index), a
   severe weather index used to determine the likelihood of severe
   thunderstorms and tornadoes (Miller, 1972).
-  This convective index is made up of a stability term (totals-totals
   index), a humidity at low levels term, wind speed terms and a shear
   term.
-  The combination of those three terms allows to distinguish severe
   thunderstorms from the ordinary thunderstorms, whose potential can be
   evaluated by the Total Totals index or the lifted index.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Air temperature, TT at 850 mb and 500 mb
-  UU wind component (along the x axis) at 850 mb and 500 mb
-  VV wind component (along the y axis) at 850 mb and 500 mb
   **and** one of the following fields at 850 mb:
-  Specific Humidity, HU
-  Water vapour mixing ratio, QV
-  Relative Humidity, HR
-  Dew point temperature, TD
-  Dew point depression, ES ***Note:*** : Make sure to provide the
   dependencies listed above to this plug-in or to the plug-in results
   called by this
   plug-in (see the section "this plug-in uses"). For more details on
   this alternative use, see the <a
   href="\ https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F

**Result(s):**

-  SWEAT index, SW (scalar, without units)

**Algorithm:**

.. code-block:: text

          For TTI, the Total Totals index.
          For TD850, the dew point temperature (deg C) at 850 mb.
          For UV850 and UV500, the wind modulus (knots) at 850 mb and 500 mb respectively.
          For WD850 and WD500, the wind direction (deg) at 850 mb and 500 mb respectively.

          *If the input fields are the specific humidity, HU (kg kg-1) or
              the water vapour mixing ratio, QV (kg kg-1) or
              the relative humidity, HR (fraction) or
              the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C) and
              wind components, UU and VV:

              Calculate the dew point temperature, TD (deg C) with TemperatureDewPoint plug-in with --iceWaterPhase WATER.

              The SWEAT index (SW) is calculated according to the equation (Miller, 1972) :
                  SW = 12*TD850 + 20*(TTI-49) + 2*UV850 + UV500 + 125*(S + 0.2)
              where S = sin(WD500 - WD850)

          *If the input fields are the dew point temperature, TD (deg C) and the air temperature, TT (deg C) and wind components, UU and VV:
              The SWEAT index (SW) is calculated according to the equation (Miller, 1972) :
                  SW = 12*TD850 + 20*(TTI-49) + 2*UV850 + UV500 + 125*(S + 0.2)
              where S = sin(WD500 - WD850)

          The term [12*TD850] = 0 if TD850 < 0
          The instability term [20*(TTI-49)] = 0 if TTI < 49
          The shear term [125*(S + 0.2)] = 0 if one of the following conditions is not satisfied :
              130 deg <= WD850 <= 250 deg
              210 deg <= WD500 <= 310 deg
              WD500 - WD850 > 0
              UV850  15 knots and UV500  15 knots

          ATTENTION: The SWEAT Index is very sensitive to TD850. Significant differences in the SWEAT value may be due to the choice
                     of the humidity variable used to calculate TD850. The algorithm of the TemperatureDewPoint plug-in describes
                     the priority used in the choice of the humidity variable needed to calculate the temperature dew point.

**Reference:**

-  `Severe Weather Forecasting:Post-Processing NWP outputs and guidance
   at the CMC; R. Verret, G. Desautels, A.
   Bergeron <https://wiki.cmc.ec.gc.ca/w/images/d/dd/Spooki_-_Severe_Weather_Forecasting.pdf>`__
-  Djurik,D 1994:Weather Analysis, Prentice-Hall.
-  `Wikipedia : SWEAT index (link only in
   French) <http://fr.wikipedia.org/wiki/Indice_de_menace_de_temps_violent>`__

**Keywords:**

-  MÉTÉO/WEATHER, stabilité/stability, convection, indice/index,
   violent/severe, orage/thunderstorm, tornade/tornado

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SweatIndex/testsFiles/inputFile.std] >>
                    [SweatIndex] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `George
   Karaganis <https://wiki.cmc.ec.gc.ca/wiki/User:Karaganisg>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `SweatIndex <classSweatIndex.html>`__
:sup:``[code] <SweatIndex_8cpp_source.html>`__`

Units tests

`Evaluation tree <SweatIndex_graph.png>`__

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
