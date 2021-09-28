=============================
Spooki: BulletinFBPreparation
=============================

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

`BulletinFBPreparation <classBulletinFBPreparation.html>`__

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

`Français <../../spooki_french_doc/html/pluginBulletinFBPreparation.html>`__

**Description:**

-  Preparation of wind and temperature data, interpolated on an ensemble
   of Canadian stations and at 3000, 6000, 9000, 12000 and 18000 heights
   (in feet), in order to write the FBCN CWAO bulletins at 06, 12 and
   24h, and/or to produce the imagery for aviation

**Iteration method:**

-  Does not apply

**Dependencies:**

-  UU wind component (along the X axis)
-  VV wind component (along the Y axis)
-  Air temperature, TT
-  Geopotential height, GZ
   ***Note:*** The wind modulus (UV) and the meteorological wind
   direction (WD) cannot be provided in dependencies to this plug-in
   (see algorithm).

**Result(s):**

-  Wind modulus UV (knots) calculated at the stations and at 3000, 6000,
   9000, 12000 and 18000 heights (in feet)
-  Meteorological wind direction WD (deg) calculated at the stations and
   at 3000, 6000, 9000, 12000 and 18000 heights (in feet)
-  Air temperature TT (deg C), interpolated at the stations and at 3000,
   6000, 9000, 12000 and 18000 heights (in feet)
-  Geopotential height GZ (dam) at the the surface, interpolated at the
   stations
-  TerrainElevation field (feet) regrouping the terrain elevation of
   each of the stations
-  StationAlphaID field (maximum of 4 letters) regrouping the
   identification codes of each of the stations
-  FictiveStationFlag boolean field indicating the real or fictitious
   status of each of the stations

**Algorithm:**

-  Interrogation of the database of stations to extract at each of the
   stations used for the FB bulletins : The latitudes of the stations
   (signed decimal degrees) The longitudes of the stations (signed
   decimal degrees)
-  Bi-cubic horizontal interpolation at the selected stations of the UU,
   VV, TT and GZ fields
-  Linear vertical interpolation of the UU, VV, and TT fields at 3000,
   6000, 9000, 12000 and 18000 heights (in feet), converted into meters,
   for the interpolation of geometric height
-  Calculation of UV and WD, from UU and VV at each point (lat,lon)
   associated to each station, defined on a reference grid of "cloud of
   points" type (corresponding to a L grid type in the particular case
   of standard files)
-  Interrogation of the database to obtain the following additional
   fields, necessary to the writing of the bulletins : The terrain
   elevation of each station (meters) The identification code of each
   station (maximum of 4 letters) A boolean field indicating for each of
   the stations if it is or is not a fictitious station

**Keywords:**

-  PRODUIT/PRODUCT, aviation, bulletin, vent/wind,
   température/temperature, FBCN, station, interpolation,
   préparation/preparation, verticale/vertical

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/BulletinFBPreparation/testsFiles/inputFile.std] >>
                    [BulletinFBPreparation] >>
                    [WriterAsciiBulletinFB --outputPath /tmp/]"
        ...

**Results validation:**

-  ...

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `BulletinFBPreparation <classBulletinFBPreparation.html>`__
:sup:``[code] <BulletinFBPreparation_8cpp_source.html>`__`

Units tests

`Evaluation tree <BulletinFBPreparation_graph.png>`__

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
