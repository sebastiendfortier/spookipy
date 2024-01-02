=================================
Spooki: TemperatureOfLiftedParcel
=================================

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

`TemperatureOfLiftedParcel <classTemperatureOfLiftedParcel.html>`__

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

`Français <../../spooki_french_doc/html/pluginTemperatureOfLiftedParcel.html>`__

**Description:**

-  Calculation of lifted parcel temperature in the vertical starting
   from the lifted parcel level (LPL).

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature (2D) at the initial lifted parcel level, TT
   **and** one of the following fields (2D) at the initial lifted parcel
   level:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR

   ***Note:*** : Make sure to include the dependencies mentioned above
   to the plug-in, or the plug-ins results called by this plug-in (see
   the section "This plug-in uses"). For more details on this
   alternative use, see the
   `page. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__

**Result(s):**

-  TTLP; temperature of the lifted parcel (deg C)
   or DTLP (deg C) when using "--liftedFrom USER\_DEFINED"
   or MTLP (deg C) when using "--liftedFrom MEAN\_LAYER"
   or UTLP (deg C) when using "--liftedFrom MOST\_UNSTABLE"
-  TVLP; virtual temperature of the lifted parcel (deg C)
   or DVLP (deg C) when using "--liftedFrom USER\_DEFINED"
   or MVLP (deg C) when using "--liftedFrom MEAN\_LAYER"
   or UVLP (deg C) when using "--liftedFrom MOST\_UNSTABLE"

| When using "--liftedFrom SURFACE" or "--liftedFrom USER\_DEFINED":

-  TT (deg C)    , parcel temperature (2D) at the LPL (lifting parcel
   level)
-  VT (deg C)    , parcel virtual temperature (2D) at the LPL
-  PX    (hPa),    parcel pressure (2D) at the LPL
-  TLCL (deg C), parcel temperature (2D) at the LCL (lifting
   condensation level)
-  TVCL (deg C), parcel virtual temperature (2D) at the LCL
-  PLCL (hPa),    parcel (2D) pressure at the LCL

| When using "--liftedFrom MEAN\_LAYER":

-  MLTT (deg C), mean layer parcel temperature (2D) at the LPL
-  MLVT (deg C), mean layer parcel virtual temperature (2D) at the LPL
-  MLPX (hPa),   mean layer parcel pressure (2D) at the LPL
-  MTCL (deg C), mean layer parcel temperature (2D) at the LCL
-  MVCL (deg C), mean layer parcel virtual temperature (2D) at the LCL
-  MPCL (hPa),   mean layer parcel pressure (2D) at the LCL

| When using "–liftedFrom MOST\_UNSTABLE:

-  MUTT (deg C), most unstable parcel temperature (2D) at the LPL
-  MUVT (deg C), most unstable parcel virtual temperature (2D) at the
   LPL
-  MUPX (hPa),   most unstable parcel pressure (2D) at the LPL
-  UTCL (deg C), most unstable parcel temperature (2D) at the LCL
-  UVCL (deg C), most unstable parcel virtual temperature (2D) at the
   LCL
-  UPCL (hPa),  most unstable parcel pressure (2D) at the LCL

**     Note :** All temperatures of a lifted parcel that cannot be
calculated will be set to -300.

| **Algorithm:**

-  https://wiki.cmc.ec.gc.ca/w/images/e/eb/Spooki_-_Algorithme_TemperatureOfLiftedParcel.odt
-  https://wiki.cmc.ec.gc.ca/w/images/c/c4/Spooki_-_Algorithme_TemperatureOfLiftedParcel.pdf

**Reference:**

-  `Alduchov, O. A., and R. E. Eskridge, 1996: Improved Magnus form
   approximation of saturation vapor pressure. J. Appl. Meteor., 35,
   601-609. <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__
-  Bluestein, H. B., 1992: Synoptic-Dynamic Meteorology in Midlatitudes
   Volume 1: Principles of Kinematics and Dynamics. Oxford University
   Press, 431 pp.
-  `Bolton, D. 1980: The computation of equivalent potential
   temperature. Mon. Wea. Rev., 108,
   1046-1053. <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0493%281980%29108%3C1046%3ATCOEPT%3E2.0.CO%3B2>`__
-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology in
   Midlatitudes. Wiley-Blackwell, 407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature, mouillée/moist, sécher/dry,
   adiabatique/adiabatic, pseudoadiabatique/pseudoadiabatic/,
   parcellesoulevée/liftedparcel, convection

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureOfLiftedParcel/testsFiles/inputFile.std] >>
                    [TemperatureOfLiftedParcel --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`TemperatureOfLiftedParcel <classTemperatureOfLiftedParcel.html>`__
:sup:``[code] <TemperatureOfLiftedParcel_8cpp_source.html>`__`

Units tests

`Evaluation tree <TemperatureOfLiftedParcel_graph.png>`__

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
