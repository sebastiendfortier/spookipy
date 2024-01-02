==========================
Spooki: ConvectiveEnergies
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

`ConvectiveEnergies <classConvectiveEnergies.html>`__

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

`Français <../../spooki_french_doc/html/pluginConvectiveEnergies.html>`__

**Description:**

-  Calculates CAPE (Convective Available Potential Energy), CIN
   (Convective Inhibition), and selected variations of them.
-  The plug-in is designed generically to apply to any parcel such as
   one lifted from the surface, one representing the mean of a layer,
   the most-unstable parcel and/or any parcel(s) defined by the user.
-  By default, the energy is calculated along the whole column up to 10
   hPa.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature, TT
-  Geopotential height, GZ
-  Geopotential Height at the surface, GZ (2D) or GZG if GZ at surface
   is unavailable and one of the following fields:
   **and** one of the following fields:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR

**Result(s):**

-  **using** the virtual temperature correction:

   -  VCP (J kg-1), the sum of all the positive buoyant energy layers in
      a column, when using "--liftedFrom SURFACE"
      or DVCP (J kg-1) when using "--liftedFrom USER\_DEFINED"
      or MVCP (J kg-1) when using "--liftedFrom MEAN\_LAYER"
      or UVCP (J kg-1) when using "--liftedFrom MOST\_UNSTABLE"
   -  VCN (J kg-1), convective inhibition defined from the lifting
      parcel level (LPL) to the level of free convection (LFC), when
      using "--liftedFrom SURFACE"
      or DVCN (J kg-1) when using "--liftedFrom USER\_DEFINED"
      or MVCN (J kg-1) when using "--liftedFrom MEAN\_LAYER"
      or UVCN (J kg-1) when using "--liftedFrom MOST\_UNSTABLE"

      -  **if** outputLevelsConvection key is used:

         -  PVC (hPa), pressure at the level of free convection (LFC),
            when using "--liftedFrom SURFACE"
            or DPVC (hPa) when using "--liftedFrom USER\_DEFINED"
            or MPVC (hPa) when using "--liftedFrom MEAN\_LAYER"
            or UPVC (hPa) when using "--liftedFrom MOST\_UNSTABLE"
         -  ZVC (m), height above ground of the optimal free convection
            (LFC), when using "--liftedFrom SURFACE"
            or DZVC (m) when using "--liftedFrom USER\_DEFINED"
            or MZVC (m) when using "--liftedFrom MEAN\_LAYER"
            or UZVC (m) when using "--liftedFrom MOST\_UNSTABLE"
         -  PVE (hPa), pressure at the EL, when using "--liftedFrom
            SURFACE"
            or DPVE (hPa) when using "--liftedFrom USER\_DEFINED"
            or MPVE (hPa) when using "--liftedFrom MEAN\_LAYER"
            or UPVE (hPa) when using "--liftedFrom MOST\_UNSTABLE"
         -  ZVE (m), height above ground of the EL, when using
            "--liftedFrom SURFACE"
            or DZVE (m) when using "--liftedFrom USER\_DEFINED"
            or MZVE (m) when using "--liftedFrom MEAN\_LAYER"
            ou UZVE (m) when using "--liftedFrom MOST\_UNSTABLE"

-  **not using** the virtual temperature correction:

   -  CAPE (J kg-1), the sum of all the positive buoyant energy layers
      in a column, when using "--liftedFrom SURFACE"
      or DCP (J kg-1) when using "--liftedFrom USER\_DEFINED"
      or MCP (J kg-1) when using "--liftedFrom MEAN\_LAYER"
      or UCP (J kg-1) when using "--liftedFrom MOST\_UNSTABLE"
   -  CINH (J kg-1), convective inhibition defined from the lifting
      parcel level (LPL) to the level of free convection (LFC), when
      using "--liftedFrom SURFACE"
      or DCN (J kg-1) when using "--liftedFrom USER\_DEFINED"
      or MCN (J kg-1) when using "--liftedFrom MEAN\_LAYER"
      or UCN (J kg-1) when using "--liftedFrom MOST\_UNSTABLE"

      -  **if** outputLevelsConvection key is used:

         -  PFC (hPa), pressure at the LFC, when using "--liftedFrom
            SURFACE"
            or DPFC (hPa) when using "--liftedFrom USER\_DEFINED"
            or MPFC (hPa) when using "--liftedFrom MEAN\_LAYER"
            or UPFC (hPa) when using "--liftedFrom MOST\_UNSTABLE"
         -  ZFC (m), height above ground of the LFC, when using
            "--liftedFrom SURFACE"
            or DZFC (m) when using "--liftedFrom USER\_DEFINED"
            or MZFC (m) when using "--liftedFrom MEAN\_LAYER"
            or UZFC (m) when using "--liftedFrom MOST\_UNSTABLE"
         -  PEL (hPa), pressure at the EL, when using "--liftedFrom
            SURFACE"
            or DPEL (hPa) when using "--liftedFrom USER\_DEFINED"
            or MPEL (hPa) when using "--liftedFrom MEAN\_LAYER"
            or UPEL (hPa) when using "--liftedFrom MOST\_UNSTABLE"
         -  ZEL (m), height above ground of the EL, when using
            "--liftedFrom SURFACE"
            or DZEL (m) when using "--liftedFrom USER\_DEFINED"
            or MZEL (m) when using "--liftedFrom MEAN\_LAYER"
            or UZEL (m) when using "--liftedFrom MOST\_UNSTABLE"

**     Note :** Undefined values associated with CAPE are set to -1
while undefined values associated with CINH are set to +1. Undefined
levels associated with LFC and EL are set to -300.

| **Algorithm:**

-  https://wiki.cmc.ec.gc.ca/w/images/a/a9/SPOOKI_-_Algorithme_ConvectiveEnergies.odt
-  https://wiki.cmc.ec.gc.ca/w/images/2/2d/SPOOKI_-_Algorithme_ConvectiveEnergies.pdf

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
   parcellesoulevée/liftedparcel, convection, CAPE, CIN

**Usage:**

| 

    | **Notes :**

    -  The use of data in pressure coordinates is not allowed with the
       –base SURFACE as this may produce unreliable results.
    -  For unbounded energy layers:

       -  The verticalLevel (IP1 in RPN STD files) will indicate the
          surface, the base of the of the mean layer or the base of the
          search for the most unstable layer.
       -  The userDefinedIndex (IP3 in RPN STD files) will be the value
          of 10mb.

    -  For bounded energy layers(positive energy only) :

       -  The verticalLevel (IP1 in RPN STD files) will indicate the
          value of the lower bound.
       -  The userDefinedIndex (IP3 in RPN STD files) will indicate the
          height difference or temperature difference OR (if encoded)
          upper bound height or upper bound temperature.

    -  For levels of free convection and equilibrium (when
       outputConvectiveLevels is used):

       -  The userDefinedIndex (IP3 in RPN STD files) will indicate the
          surface, the base of the mean layer or most unstable layer.

    -  When using the –MeanLayer and –MostUnstable options:

       -  Characters 2 to 4 of the pdsLabel (5 to 8 of the etiket in RPN
          STD files) will indicate the thickness of the mean layer or
          the thickness of the most unstable layer. The last character
          indicates the units (P for hPa above the base of the layer and
          Z for meters above the base of the layer).

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ConvectiveEnergies/testsFiles/inputFile.std] >>
                    [ConvectiveEnergies --liftedFrom SURFACE --endLevel 10.0hPa --increment 10.0hPa --virtualTemperature NO] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

-  ...

**Contacts:**

-  Author : Neil Taylor
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `ConvectiveEnergies <classConvectiveEnergies.html>`__
:sup:``[code] <ConvectiveEnergies_8cpp_source.html>`__`

Units tests

`Evaluation tree <ConvectiveEnergies_graph.png>`__

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
