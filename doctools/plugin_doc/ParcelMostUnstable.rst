==========================
Spooki: ParcelMostUnstable
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

`ParcelMostUnstable <classParcelMostUnstable.html>`__

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

`Français <../../spooki_french_doc/html/pluginParcelMostUnstable.html>`__

**Description:**

-  Calculation of the characteristics of the most-unstable parcel of the
   column, within a user defined depth.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature in the probed layer, TT
-  Geopotential height in the probed layer, GZ and one of the following
   fields in the probed layer:
-  Specific humidity, HU
-  Relative humidity, HR
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES

**Result(s):**

-  Temperature of the most-unstable parcel, MUTT (deg C)
-  Dew point of the most-unstable parcel, MUTD (deg C)
-  `Pressure <classPressure.html>`__ of the most-unstable parcel, MUPX
   (hPa)
-  Relative humidity of the most-unstable parcel, MUHR (fraction)
-  Height above the surface of the most-unstable parcel, MUZ (m)
-  The maximum wet-bulb potential temperature in the column, TWMX (deg
   C)

**Algorithm:**

.. code-block:: text

        Call the Pressure plug-in to obtain PX (hPa) in the probed layer.
        Call the TemperatureWetBulb plug-in to obtain TTW (deg C) in the probed layer.

        Call the InterpolationVertical plug-in with --verticalLevelType MILLIBARS_ABOVE_LEVEL
                                                    --referenceLevel SURFACE
                                                    --verticalLevel (value of --delta)
                                                    --interpolationType LINEAR
                                                    --extrapolationType ABORT
                 to find the value of the input fields for the highest level or the probed layer.

        Call the TemperatureWetBulb plug-in to obtain TTW (deg C) for the highest level or the probed layer (with interpolated TT and the chosen humidity field interpolated).

        Initialise TWMX = -999.0
        For each level between the surface and "delta" above the surface:
           Calculate TW (deg C) with the TemperatureWetBulbPotential function.
           If TW > TWMX:
              TWMX = TW
              MUZ (m) = (GZ (dam) - GZsurface (dam)) * 10 (m/dam)
              Replace the values of the following output fields by those at the current level: MUTT, MUPX and the chosen humidity field.

        Call the TemperatureDewPoint and HumidityRelative plug-ins with TT=MUTT, PX=MUPX and the chosen humidity field.

        Call the Zap plug-in to rename HR by MUHR et TD by MUTD.

**Références :**

-  Doswell, C. A. and E. N. Rasmussen, 1994: The effect of neglecting
   the virtual temperature correction on CAPE calculations. Wea.
   Forecasting, 9, 625-629.

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature,
   parcellesoulevée/liftedparcel, plusinstable/mostunstable, convection

**Usage:**

    | 
    | **Notes :**
    | The use of data in pressure coordinates is not allowed as this may
      produce unreliable results.
    | Information about the metadata:

    -  The verticalLevel (IP1 in RPN STD files) will indicate the base
       of the search for the most unstable layer.
    -  Characters 2 to 4 of the pdsLabel (5 to 8 of the etiket in RPN
       STD files) will indicate the thickness of the most unstable
       layer. The last character indicates the units (P for hPa above
       the base of the layer and Z for meters above the base of the
       layer).

    **Call example:** ````

    ::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ParcelMostUnstable/testsFiles/inputFile.std] >>
                        [ParcelMostUnstable --delta 100mb --iceWaterPhase WATER] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
            ...

    **Results validation:**

    **Contacts:**

    -  Author : Neil Taylor
    -  Coded by : `Jonathan
       St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to `ParcelMostUnstable <classParcelMostUnstable.html>`__
    :sup:``[code] <ParcelMostUnstable_8cpp_source.html>`__`

    Unit Tests

    | **Uses:**

    | **Used by:**

    --------------

    Generated by  |doxygen| 1.8.13

.. raw:: html

   </div>

.. raw:: html

   </div>

.. |doxygen| image:: doxygen.png
   :class: footer
   :target: http://www.doxygen.org/index.html
