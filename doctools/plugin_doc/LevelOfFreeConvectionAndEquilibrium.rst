===========================================
Spooki: LevelOfFreeConvectionAndEquilibrium
===========================================

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

`LevelOfFreeConvectionAndEquilibrium <classLevelOfFreeConvectionAndEquilibrium.html>`__

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

`Français <../../spooki_french_doc/html/pluginLevelOfFreeConvectionAndEquilibrium.html>`__

**Description:**

-  Calculation of level(s) of free convection (LFC) and/or equilibrium
   level(s) (EL) based on a comparison of environmental and lifted
   parcel virtual temperatures. Results not using the virtual
   temperature correction are also available. The plug-in allows for the
   LFC to be at the surface in the case of a superadiabatic layer and
   allows multiple LFCs and/or ELs corresponding to multiple unstable
   layers (parcel temperature warmer than environment temperature).
-  The plug-in is designed generically to apply to any parcel such as
   one lifted from the surface, one representing the mean of a layer,
   the most-unstable parcel and/or any parcel(s) defined by the user.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature of the environment, TT (3D)
-  Geopotential height of the environment, GZ (3D)
-  Geopotential height of the ground, GZ (2D) (or GZG if GZ of the
   ground is not available)
   **and** one of the following fields of the environment:
-  Specific humidity, HU (3D)
-  Water vapour mixing ratio, QV (3D)
-  Dew point temperature, TD (3D)
-  Dew point depression, ES (3D)
-  Relative humidity, HR (3D)

**Result(s):**

-  **using** the virtual temperature correction:

   -  NVC (2D), number of levels of free convection (LFC), when using
      "--liftedFrom SURFACE"
      or DNVC (2D) when using "--liftedFrom USER\_DEFINED"
      or MNVC (2D) when using "--liftedFrom MEAN\_LAYER"
      or UNVC (2D) when using "--liftedFrom MOST\_UNSTABLE"
   -  PVC(hPa), pressure at the level of free convection (LFC), when
      using "--liftedFrom SURFACE"
      or DPVC (hPa) when using "--liftedFrom USER\_DEFINED"
      or MPVC (hPa) when using "--liftedFrom MEAN\_LAYER"
      or UPVC (hPa) when using "--liftedFrom MOST\_UNSTABLE"
   -  ZVC (m), height above ground of the level of free convection
      (LFC), when using "--liftedFrom SURFACE"
      or DZVC (m) when using "--liftedFrom USER\_DEFINED"
      or MZVC (m) when using "--liftedFrom MEAN\_LAYER"
      or UZVC (m) when using "--liftedFrom MOST\_UNSTABLE"
   -  NVE (2D), number of levels of equilibrium (EL),when using
      "--liftedFrom SURFACE"
      or DNVE (2D) when using "--liftedFrom USER\_DEFINED"
      or MNVE (2D) when using "--liftedFrom MEAN\_LAYER"
      or UNVE (2D) when using "--liftedFrom MOST\_UNSTABLE"
   -  PVE (hPa), pressure at the equilibrium level (EL), when using
      "--liftedFrom SURFACE"
      or DPVE (hPa) when using "--liftedFrom USER\_DEFINED"
      or MPVE (hPa) when using "--liftedFrom MEAN\_LAYER"
      or UPVE (hPa) when using "--liftedFrom MOST\_UNSTABLE"
   -  ZVE (m), height above ground of the equilibrium level (EL), when
      using "--liftedFrom SURFACE"
      or DZVE (m) when using "--liftedFrom USER\_DEFINED"
      or MZVE (m) when using "--liftedFrom MEAN\_LAYER"
      or UZVE (m) when using "--liftedFrom MOST\_UNSTABLE"

-  **not** using the virtual temperature correction:

   -  NLFC (2D), number of levels of free convection(LFC), when using
      "--liftedFrom SURFACE"
      or DNFC (2D) when using "--liftedFrom USER\_DEFINED"
      or MNFC (2D) when using "--liftedFrom MEAN\_LAYER"
      or UNFC (2D) when using "--liftedFrom MOST\_UNSTABLE"
   -  PFC(hPa), pressure at the level of free convection (LFC), when
      using "--liftedFrom SURFACE"
      or DPFC (hPa) when using "--liftedFrom USER\_DEFINED"
      or MPFC (hPa) when using "--liftedFrom MEAN\_LAYER"
      or UPFC (hPa) when using "--liftedFrom MOST\_UNSTABLE"
   -  ZFC (m), height above ground of the level of free convection
      (LFC), when using "--liftedFrom SURFACE"
      or DZFC (m) when using "--liftedFrom USER\_DEFINED"
      or MZFC (m) when using "--liftedFrom MEAN\_LAYER"
      or UZFC (m) when using "--liftedFrom MOST\_UNSTABLE"
   -  NEL (2D), number of levels of equilibrium (EL),when using
      "--liftedFrom SURFACE"
      or DNEL (2D) when using "--liftedFrom USER\_DEFINED"
      or MNEL (2D) when using "--liftedFrom MEAN\_LAYER"
      or UNEL (2D) when using "--liftedFrom MOST\_UNSTABLE"
   -  PEL (hPa), pressure at the equilibrium level (EL), when using
      "--liftedFrom SURFACE"
      or DPEL (hPa) when using "--liftedFrom USER\_DEFINED"
      or MPEL (hPa) when using "--liftedFrom MEAN\_LAYER"
      or UPEL (hPa) when using "--liftedFrom MOST\_UNSTABLE"
   -  ZEL (m), height above ground of the equilibrium level (EL), when
      using "--liftedFrom SURFACE"
      or DZEL (m) when using "--liftedFrom USER\_DEFINED"
      or MZEL (m) when using "--liftedFrom MEAN\_LAYER"
      or UZEL (m) when using "--liftedFrom MOST\_UNSTABLE"

**     Note :** Undefined levels associated with LFC and EL are set to
-300.

**Algorithm:**

-  https://wiki.cmc.ec.gc.ca/w/images/3/3b/SPOOKI_-_Algorithme_LevelOfFreeConvectionAndEquilibrium.odt
-  https://wiki.cmc.ec.gc.ca/w/images/3/37/SPOOKI_-_Algorithme_LevelOfFreeConvectionAndEquilibrium.pdf

**Reference:**

-  Doswell, C. A. and E. N. Rasmussen, 1994: The effect of neglecting
   the virtual temperature correction on CAPE calculations. Wea.
   Forecasting, 9, 625-629.
-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology in
   Midlatitudes. Wiley-Blackwell, 407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature,
   parcellesoulevée/liftedparcel, pression/pressure, convection,
   niveau/level

**Usage:**

    | 
    | ***Note :***
    | The use of data in pressure coordinates is not allowed with the
      –base SURFACE as this may produce unreliable results.
    | When the –MeanLayer and –MostUnstable are used:

    -  The userDefinedIndex (IP3 in RPN STD files) will indicate the
       base of the mean layer or the base of the search for the most
       unstable layer.
    -  Characters 5 to 7 of the etiket indicate the thickness of the
       mean layer or the thickness of the search layer for the most
       unstable layer
    -  Character 8 of the etiket indicates the units that apply to
       characters 5 to 7 of the eitket (P for hPa above the base of the
       layer, Z for meters above the base of the layer)

    **Call example:** ````

    ::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/LevelOfFreeConvectionAndEquilibrium/testsFiles/inputFile.std] >>
                        [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa --virtualTemperature NO --outputField LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT --outputLevels MULTIPLE_VALUES] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
            ...

    **Results validation:**

    **Contacts:**

    -  Author : Neil Taylor : `Khanh-Hung
       Lam <https://wiki.cmc.ec.gc.ca/wiki/User:Lamk>`__
    -  Coded by : `Jonathan
       St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__ `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to
    `LevelOfFreeConvectionAndEquilibrium <classLevelOfFreeConvectionAndEquilibrium.html>`__
    :sup:``[code] <LevelOfFreeConvectionAndEquilibrium_8cpp_source.html>`__`

    Unit tests

    `Evaluation tree <LevelOfFreeConvectionAndEquilibrium_graph.png>`__

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
