=======================
Spooki: ParcelMeanLayer
=======================

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

`ParcelMeanLayer <classParcelMeanLayer.html>`__

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

`Français <../../spooki_french_doc/html/pluginParcelMeanLayer.html>`__

**Description:**

-  Calculation of the temperature, dew point temperature, relative
   humidity, pressure and height of a mean-layer parcel.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature covering the layer desired, TT (3D)
-  Geopotential height covering the layer desired, GZ (3D)
-  Geopotential height of the ground, GZ (2D) (or GZG if GZ of the
   ground is not available)

| **and** one of the following fields covering the layer desired:

-  Specific humidity, HU (3D)
-  Relative humidity, HR (3D)
-  Water vapour mixing ratio, QV (3D)
-  Dew point temperature, TD (3D)
-  Dew point depression, ES (3D)
   ***Note:*** : Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results
   called by this plug-in (see the section "this plug-in uses"). For
   more details on this alternative use,
   see the `documentation
   page. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

**Result(s):**

-  Temperature of the mean layer parcel, MLTT (deg C)
-  Dew point of the mean layer parcel, MLTD (deg C)
-  Pressure of the mean layer parcel, MLPX (hPa)
-  Relative humidity of the mean layer parcel, MLHR (fraction)
-  Height above ground of the mean layer parcel, MLZ (m)

**Algorithm:**

    | Call the plug-in `Pressure <classPressure.html>`__ to obtain PX
      (hPa) in the layer.
    | Call the plug-in `HumiditySpecific <classHumiditySpecific.html>`__
      to obtain HU (kg/kg), if HU is not available.
    | Call the linear interpolation functions (on ln P and with no
      extrapolation allowed) to obtain the values of the fields found on
      the levels in the desired layer, if these fields are not in the
      input data.

    Calculate MLTT, MLPX and MLZ:

        | TT - temperature (deg C)
        | HU - specific humidity(kg/kg)
        | TD - temperature dew point (deg C)
        | HR - relative humidity(fraction)
        | GZ - geopotential height (dam)
        | Ki - initial level of the mean layer (given by –base)
        | Kt - final level of the mean layer (given by –base and –delta)
        | N - numbers of levels between Ki and Kt (given by the data in
          the input)

        | \\( MLTT = \\frac {\\sum\_{Ki}^{Kt} TT}{N+1}\\)
        | \\( MLPX = \\frac {\\sum\_{Ki}^{Kt} PX}{N+1}\\)
        | \\( MLZ = ( \\frac {\\sum\_{Ki}^{Kt} GZ}{N+1} - GZ(ground) )
          \*10.0 \\)

    | Calculate MLTD and MLHR:

        \\( MLHU = \\frac {\\sum\_{Ki}^{Kt} HU}{N+1} \\)
        Call the plug-ins
        `TemperatureDewPoint <classTemperatureDewPoint.html>`__ and
        `HumidityRelative <classHumidityRelative.html>`__ to obtain TD
        and HR with:
              TT = MLTT
              HU = MLHU
              PX = MLPX
        Call the plug-in `Zap <classZap.html>`__ to rename TD by MLTD
        and HR by MLHR.

**References:**

-  Craven, J. P., R. E. Jewell, and H. E. Brooks, 2002: Comparison
   between observed convective cloud-base heights and lifting
   condensation level for two different lifted parcels. Wea.
   Forecasting, 17, 885-890.

**Keywords:**

-  MÉTÉO/WEATHER, parcelle/parcel, couchemoyenne/meanlayer, convection,
   température/temperature, pression/pressure, humidité/humidity,
   pointderosée/dewpoint, hauteur/height

**Usage:**

    | 
    | **Notes :**
    | The use of data in pressure coordinates is not allowed with the
      –base SURFACE as this may produce unreliable results.
    | Information about the metadata:

    -  The verticalLevel (IP1 in RPN STD files) will indicate the base
       of the mean layer.
    -  Characters 2 to 4 of the pdsLabel (5 to 8 of the etiket in RPN
       STD files) will indicate the thickness of the mean layer. The
       last character indicates the units (P for hPa above the base of
       the layer and Z for meters above the base of the layer).

    **Call example:** ````

    ::

                ...
                spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ParcelMeanLayer/testsFiles/inputFile.std] >>
                            [ParcelMeanLayer --base SURFACE --delta 100mb --iceWaterPhase WATER] >>
                            [WriterStd --output /tmp/$USER/outputFile.std]"
                ...
            

    **Results validation:**

    **Contacts:**

    -  Author : Neil Taylor
    -  Coded by : `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to `ParcelMeanLayer <classParcelMeanLayer.html>`__
    :sup:``[code] <ParcelMeanLayer_8cpp_source.html>`__`

    Unit Tests

    `Evaluation tree <ParcelMeanLayer_graph.png>`__

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
