===================
Spooki: LiftedIndex
===================

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

`LiftedIndex <classLiftedIndex.html>`__

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

`Français <../../spooki_french_doc/html/pluginLiftedIndex.html>`__

**Description:**

-  Calculation of the lifted index based on the difference between
   environmental and lifted parcel virtual temperature at the reference
   level given by –referenceLevel (default: 500 hPa). This version of
   the lifted index is generalized to be applied to the surface-based,
   mean-layer, or most-unstable lifted parcel levels as well as
   calculate the Showalter Index. Output of lifted index based on
   temperature (i.e., not using the virtual temperature correction) is
   also available. The calculation can be performed at different
   heights.
-  Stability index gives as an indication on the possibility of severe
   weather occurrences (thunderstorms, etc...)

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature to calculate values at the lifted parcel level and
   the –referenceLevel , TT
-  `Pressure <classPressure.html>`__ field to calculate values at the
   lifted parcel level and the –referenceLevel , PX
   **and** one of the following fields to calculate values at the lifted
   parcel level and the –referenceLevel:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR
   ***Note:*** : Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results
   called by this plug-in (see the section "this plug-in uses"). For
   more details on this alternative use,
   see the `documentation
   page. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

**Result(s):**

-  Lifted index for the surface based parcel calculated using the
   virtual temperature correction, VLI (deg K)
-  Lifted index for the surface based parcel calculated using the
   temperature, LI (deg K)
-  Lifted index for the mean layer parcel calculated using the virtual
   temperature correction, MVLI (deg K)
-  Lifted index for the mean layer parcel calculated using the
   temperature, MLI (deg K)
-  Lifted index for the most unstable parcel calculated using the
   virtual temperature correction, UVLI (deg K)
-  Lifted index for the most unstable parcel calculated using the
   temperature, ULI (deg K)
-  Showalter index using the virtual temperature correction, VWA (deg K)
-  Showalter index using temperature, WA (deg K)

**     Note :** Undefined values for the indices are set to 99.99.

| **Algorithm:**

.. code-block:: text

        The lifted parcel level (LPL) will be specified by the parameter key --liftedFrom as one of
        the surface-based (SURFACE), mean-layer (MEAN_LAYER), most-unstable (MOST_UNSTABLE) parcel, 850hPa (SHOWALTER). Several can be done with one call, one after the other.

        For each LPL required:

        If ML or MU parcel are needed call ParcelMeanLayer or ParcelMostUnstable plug-ins otherwise choose the surface level or 850hPa for Showalter

        Use TemperatureOfLiftedParcel plug-in with the --increment argument of this plugin and the argument --referenceLevel in --endLevel) for:

           PXLP; pressure values from the LPL to the top of the lifted parcel curve (--referenceLevel)
           TTLP; temperature values from the LPL to the top of the lifted parcel curve (--referenceLevel)
           TVLP; virtual temperature values from the LPL to the top of the lifted parcel curve (--referenceLevel)

        Find the environmental virtual temperature at --referenceLevel from the input data, eTV500:
        Find the environmental temperature at --referenceLevel form the input data, eTT500

        Find the virtual temperature of the lifted parcel at --referenceLevel from the input data, pTV500
        Find the temperature of the lifted parcel at --referenceLevel from the input data, pTT500

        VLI = eTV500 - pTV500
        LI  = eTT500 - pTT500

        For mean-layer parcel: rename VLI to MVLI and LI to MLI
        For most-unstable parcel rename VLI to UVLI and LI to ULI
        For Showalter rename VLI to VWA and LI to WA

        Note 1: If the level of the most unstable parcel is above the reference level (--referenceLevel) then the
                lifted index is undefined and its value set to 99.99.

**Reference:**

-  Doswell, C. A. and E. N. Rasmussen, 1994: The effect of neglecting
   the virtual temperature correction on CAPE calculations. Wea.
   Forecasting, 9, 625-629.
-  Galway, J. G. 1956: The lifted index as a predictor of latent
   instability. Bull. Amer. Meteor. Soc., 37, 528-529.
-  Showalter, A. K. 1947. A stability index for forecasting
   thunderstorms. Bull. Amer. Meteor. Soc., 34, 250-252.
-  "Atmospheric Thermodynamics", Iribarne, J.V., and Godson, W.L.
   (Riedel, 2nd edition, 1981)
-  `Atmospheric Convection, Kerry A., Emanuel,
   1994 <http://www.books.google.com/books?id=VdaBBHEGAcMC&amp;dq=atmospheric+convection+Kerry+A+Emanuel&amp;printsec=frontcover&amp;source=bn&amp;hl=en&amp;ei=WsWsS7GEONKUtgf9rKHCDw&amp;sa=X&amp;oi=book_result&amp;ct=result&amp;resnum=5&amp;ved=0CBUQ6AEwBA#v=onepage&amp;q=&amp;f=false>`__

**Keywords:**

-  MÉTÉO/WEATHER, convection, température/temperature,
   parcellesoulevée/liftedparcel, plusinstable/mostunstable,
   couchemoyenne/meanlayer, indice/index, stabilité/stability,
   tempsviolent/severeweather, showalter

**Usage:**

**Information about the metadata:**
When the –MeanLayer and –MostUnstable options are used:

-  The verticalLevel (IP1 in RPN STD files) will indicate the base of
   the of the mean layer or the base of the search for the most unstable
   layer.
-  Characters 2 to 4 of the pdsLabel (5 to 8 of the etiket in RPN STD
   files) will indicate the thickness of the mean layer or the thickness
   of the most unstable layer. The last character indicates the units (P
   for hPa above the base of the layer and Z for meters above the base
   of the layer).

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/LiftedIndex/testsFiles/inputFile.std] >>
                    [LiftedIndex --liftedFrom SHOWALTER] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/Sandrine_Edouard>`__, Neil
   Taylor
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `LiftedIndex <classLiftedIndex.html>`__
:sup:``[code] <LiftedIndex_8cpp_source.html>`__`

Units tests

`Evaluation tree <LiftedIndex_graph.png>`__

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
