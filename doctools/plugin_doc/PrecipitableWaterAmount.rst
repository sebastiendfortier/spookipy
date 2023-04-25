===============================
Spooki: PrecipitableWaterAmount
===============================

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

`PrecipitableWaterAmount <classPrecipitableWaterAmount.html>`__

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


`Français <../../spooki_french_doc/html/pluginPrecipitableWaterAmount.html>`__

**Description:**

-  Calculation of the precipitable water content in a determined
   vertical layer. Consists of the summation of the water vapour between
   the base and the top of this layer.

**Iteration method:**

-  Column by column

| **Dependencies:**

One of the following (3D) humidity fields:

-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR
   **and**
   If the value of "--base" or "--top" is in length units:
-  Geopotential height, GZ
   If we use the option "--base SURFACE":
-  Surface air pressure, P0

**Result(s):**

-  Precipitable water amount, EP (2D field, mm)

**Algorithm:**

::

::

            For HU(k) = the specific humidity at level k in kg/kg
            For g     = gravitational acceleration (9.80616 m.s-2)
            For EP    = precipitable water in mm
            For ρ     = water density (1000 kg.m-3)

::

            If the input humidity variable is not specific humidity, call the HumiditySpecific plug-in with options --iceWaterPhase BOTH --temperaturePhaseSwitch -40C

::

            Calculate the pressure PX(k) in hPa for every HU(k) level

::

            Zstart = --base value if in length units
            Pstart = pressure level where we start calculating EP
            Zend   = --top value if in length units
            Pend   = pressure level where we stop calculating EP

::

            If the --base value is in pressure units
               Pstart = --base value converted to hPa
            If the --base value is in length units
               Pstart = --base value converted to pressure by linearly interpolating lnP between two levels
            If the value of --base = SURFACE
               Pstart = P0

::

            If the value of --top is in pressure units
               Pend = --top value converted to hPa
            If the value of --top is in length units
               Pend = --top value converted to pressure by linearly interpolating lnP between two levels
            If the value of --top = HIGHEST
               Pend = PX of the highest level in the input data

::

            To convert length unit values to pressure values:
               Convert PX for each column level in ln(PX) and send to InterpolationVertical with GZ.
               Call InterpolationVertical
                    --outputGridDefinitionMethod USER_DEFINED
                    --verticalLevel Pstart or Pend value
                    --verticalLavelType METER_GROUND_LEVEL
                    --interpolationType LINEAR
                    --extrapolationType ABORT
                    --outputField INTERPOLATED_FIELD_ONLY
               Convert the ln(PX) result into a pressure value.

::

            Check that Pstart > Pend
            EP=0

::

            Do k=first level from ground, until the last level - 1

::

               If PX(k) > Pstart and PX(K+1) > Pstart

::

                  Check that EP=0.0
                  K=K+1

::

               Else if PX(k) = Pstart

::

                  Check that EP=0.0

::

                  If PX(K+1) > Pend
                     EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
                     K=K+1
                  Else if PX(K+1) < Pend
                     Interpolate HU in lnP to find the value of HUend at Pend
                     EP = 1/(ρ*g) * 0.5 * (HUend + HU(K)) * ABS(Pend - PX(K))
                     Exit the loop
                  Else if PX(K+1) = Pend
                     EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
                     Exit the loop
                  Endif

::

               Else if PX(k) > Pstart and PX(K+1) < Pstart

::

                  Check that EP=0.0
                  Interpolate HU in lnP to find the value of HUend at Pstart

::

                  If PX(K+1) > Pend
                     EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HUstart) * ABS(PX(k+1) - Pstart)
                     K=K+1
                  Else if PX(K+1) < Pend
                     Interpolate HU in lnP to find the value of HUend at Pend
                     EP = 1/(ρ*g) * 0.5 * (HUend + HUstart) * ABS(Pend - Pstart)
                     Exit the loop
                  Else if PX(K+1) = Pend
                     EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HUstart) * ABS(PX(k+1) - Pstart)
                     Exit the loop
                  Endif

::

               Else if PX(k) < Pstart and PX(K+1) < Pstart

::

                  If PX(K+1) > Pend
                     EP = EP + 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
                     K=K+1
                  Else if PX(K+1) < Pend
                     EP = EP + 1/(ρ*g) * 0.5 * (HUend + HU(K)) * ABS(Pend - PX(K))
                     Exit the loop
                  Else if PX(K+1) = Pend
                     EP = EP + 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
                     Exit the loop
                  Endif

::

               Else
                  Error !
               End if

::

               Convert EP to mm by mutiplying by 10**5

::

       

**Reference:**

-  Taken from the operational program, eeaucol\_fstd2000.f

**Keywords:**

-  MÉTÉO/WEATHER , eau/water, quantité/amount ,
   précipitable/precipitable

**Usage:**

    **Notes :**
    The use of data in pressure coordinates is not allowed with "--base
    SURFACE" as this may produce unreliable results.

**Call example:** ````

::

           ...
           spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitableWaterAmount/testsFiles/inputFile.std] >>
                       [PrecipitableWaterAmount --base SURFACE --top HIGHEST] >>
                       [WriterStd --output /tmp/$USER/outputFile.std]"
           ...
       

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
   `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
   `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`PrecipitableWaterAmount <classPrecipitableWaterAmount.html>`__
:sup:``[code] <PrecipitableWaterAmount_8cpp_source.html>`__`

`Units tests <PrecipitableWaterAmount_8cpp.html>`__

`Evaluation tree <PrecipitableWaterAmount_graph.png>`__

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
