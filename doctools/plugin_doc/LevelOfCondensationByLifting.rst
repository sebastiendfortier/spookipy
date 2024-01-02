====================================
Spooki: LevelOfCondensationByLifting
====================================

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

`LevelOfCondensationByLifting <classLevelOfCondensationByLifting.html>`__

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

`Français <../../spooki_french_doc/html/pluginLevelOfCondensationByLifting.html>`__

**Description:**

-  This plug-in is used to calculate the lifting condensation level
   based on temperature, dewpoint and pressure for a given parcel. The
   LCL is the level where saturation occurs for a parcel undergoing
   adiabatic lift and can be found graphically on a tephigram by
   ascending from the lifting parcel level up the corresponding dry
   adiabatic and mixing ratio lines until their intersection.
-  The plug-in is designed generically to apply to any parcel such as
   one lifted from the surface, one representing the mean of a layer,
   the most-unstable parcel and/or any parcel(s) defined by the user.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Air temperature at lifting parcel level, TT
-  Geopotential height of the ground and the lifting parcel level, GZ
   (or GZG if GZ of the ground is not available)
-  Geopotential height of the lifting parcel level, GZ
   **and** one of the following fields at the lifting parcel level:
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR
   ***Note:*** Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results called by this plug-in (see
   the section "this plug-in uses"). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

**Result(s):**

-  TLCL (deg C), lifting condensation level temperature, also known as
   saturation temperature
   or MTLC (deg C) when using "--liftedFrom MEAN\_LAYER"
   or UTCL (deg C) when using "--liftedFrom MOST\_UNSTABLE"
-  PLCL (hPa), lifting condensation level pressure
   or MPCL (hPa) when using "--liftedFrom MEAN\_LAYER"
   or UPCL (hPa) when using "--liftedFrom MOST\_UNSTABLE"
-  ZLCL (m), lifting condensation level height above the surface
   or MZCL (m) when using "--liftedFrom MEAN\_LAYER"
   or UZCL (m) when using "--liftedFrom MOST\_UNSTABLE"

| **Algorithm:**

-  `LevelOfCondensationByLifting
   algorithm <https://wiki.cmc.ec.gc.ca/w/images/d/d8/SPOOKI_-_Algorithme_LevelOfCondensationByLifting.docx>`__

**Reference:**

-  `Barnes, S. L., 1968: An empirical shortcut to the calculation of
   temperature and pressure at the lifted condensation
   level. <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281968%29007%3C0511%3AAESTTC%3E2.0.CO%3B2>`__
-  Bolton, D. 1980: The computation of equivalent potential temperature.
   *Mon. Wea. Rev*., 108, 1046-1053. `Available
   online <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0493%281980%29108%3C1046%3ATCOEPT%3E2.0.CO%3B2>`__
   or
   `localy <https://wiki.cmc.ec.gc.ca/w/images/1/1a/Spooki_-_Bolton1980.pdf>`__
-  `Brunet, N., 2001: Les Fonctions Thermodynamiques et le Fichier de
   Constantes. <http://iweb.cmc.ec.gc.ca/%7Eafsypst/info_divers/doc_thermo.pdf>`__
-  "Atmospheric Thermodynamics", Iribarne, J.V., and Godson, W.L.
   (Riedel, 2nd edition, 1981)
-  `Atmospheric Convection, Kerry A., Emanuel,
   1994 <http://books.google.ca/books?id=VdaBBHEGAcMC&dq=atmospheric+convection+Kerry+A+Emanuel&printsec=frontcover&source=bn&hl=en&ei=WsWsS7GEONKUtgf9rKHCDw&sa=X&oi=book_result&ct=result&safe=images&redir_esc=y#v=onepage&q&f=false>`__
-  `Librairie thermodynamique de
   RPN <http://iweb.cmc.ec.gc.ca/%7Eafsypst/info_divers/doc_thermo.pdf>`__

**Keywords:**

-  MÉTÉO/WEATHER, condensation, ascendance/lifting , saturation,
   convection

**Usage:**

    | 
    | **Information about the metadata:**

    When the –MeanLayer and –MostUnstable options are used:

    -  The verticalLevel (IP1 in RPN STD files) will indicate the base
       of the of the mean layer or the base of the search for the most
       unstable layer.
    -  Characters 2 to 4 of the pdsLabel (5 to 8 of the etiket in RPN
       STD files) will indicate the thickness of the mean layer or the
       thickness of the most unstable layer. The last character
       indicates the units (P for hPa above the base of the layer and Z
       for meters above the base of the layer).

    **Call example:** ````

    ::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/LevelOfCondensationByLifting/testsFiles/inputFile.std] >>
                        [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom SURFACE --iceWaterPhase WATER] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
            ...

    **Results validation:**

    **Contacts:**

    -  Author : Neil Taylor
    -  Coded by : Jonathan Cameron
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to
    `LevelOfCondensationByLifting <classLevelOfCondensationByLifting.html>`__
    :sup:``[code] <LevelOfCondensationByLifting_8cpp_source.html>`__`

    Units tests

    `Evaluation tree <LevelOfCondensationByLifting_graph.png>`__

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
