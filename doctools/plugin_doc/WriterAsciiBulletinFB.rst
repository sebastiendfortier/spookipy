=============================
Spooki: WriterAsciiBulletinFB
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

`WriterAsciiBulletinFB <classWriterAsciiBulletinFB.html>`__

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

`Francais <../../spooki_french_doc/html/pluginWriterAsciiBulletinFB.html>`__

**Description:**

-  Writing of FBCN bulletins, in ASCII format, regrouping the wind and
   temperature forecasts in altitude, interpolated on an ensemble of
   Canadian stations at 3000, 6000, 9000, 12000 and 18000 heights (in
   feet). The bulletins are produced at 06h (FBCN31), 12h (FBCN33) and
   24h (FBCN35) of forecasts.
-  The backup bulletins are produced in case of problems with the two
   subsequent regional runs (current run + 6 hours and current run + 12
   hours).

**Iteration method:**

-  Does not apply

**Dependance:**

-  Wind modulus (UV) calculated at the stations and at the 3000, 6000,
   9000, 12000 and 18000 heights (in feet) at one of the forecast hours:
   6, 12, 18, 24, 30 and 36.
-  Meteorological wind direction (WD) calculated at the stations and at
   the 3000, 6000, 9000, 12000 and 18000 heights (in feet) at one of the
   forecast hours: 6, 12, 18, 24, 30 and 36.
-  Air temperature (TT) interpolated at the stations and at the 3000,
   6000, 9000, 12000 and 18000 heights (in feet) at one of the forecast
   hours: 6, 12, 18, 24, 30 and 36.
-  Geopotential height (GZ) at the surface, interpolated at the
   stations.
-  Terrain elevation (TerrainElevation) of each of the stations.
-  Latitude (LAT) of each of the stations.
-  Longitude (LON) of each of the stations.
-  Identification code (StationAlphaID) of each of the stations (code of
   a maximum of 4 letters).

NOTE: These dependencies can be first obtained by the
`BulletinFBPreparation <classBulletinFBPreparation.html>`__ plug-in.

**Result(s):**

-  A FBCN CWAO bulletin at 06h, 12h or 24h of forecast, named
   FBCN{31-33-35}.
-  Depending on the forecast hour, one or two bulletin(s) used as backup
   bulletin(s), in the case of problems with the two next operational
   regional runs (backup 6 and backup 12), named
   FBCN{31-33-35}\_backup{06-12}.
-  Inside the bulletins (regular and backup) , the stations are ordered
   in the following order : the stations south of 60N ordered from west
   to east and north to south, and the stations north of 60N ordered
   from west to east and north to south.

**Algorithm:**

.. code-block:: text

    1. Construction of the headers for each bulletin in function of the run hour and of the forecast hour (6, 12, 18, 24, 30 and 36)
       in the ASCII format predefined at 6, 12 or 24h.

       The plug-in determines the temporal components to indicate in the bulletin header, that are :

            - approximate time of output of the bulletin :
                 - time of the run + 3h20 , if the forecast hour = 6h
                 - time of the run + 3h30 , if the forecast hour = 12h or 24h

            - hour of validity = time of the run + forecast hour

            - usage period :
                 - (hour of validity - 4h) to (hour of validity + 3h) , if the forecast hour = 6h
                 - (hour of validity - 3h) to (hour of validity + 6h) , if the forecast hour = 12h
                 - (hour of validity - 6h) to (hour of validity + 6h) , if the forecast hour = 24h

    2. Writing of the concerned bulletin headers.

    3. Sort the stations : the stations south of the 60N (inclusively) are ordered from west to east and north to south, and the stations north of 60N are ordered from
       west to east and north to south.

    4. Preparation of data for each station and for each height (3000, 6000, 9000, 12000 and 18000 feet) :

          - No forecast is written at the 3000 height (in feet) if:
               - the altitude of the station is greater than 1500 feet
            or
               - the geopotential height of the station (converted into feet) is greater than or equal to 3000 feet

          - Combination of UV, WD and TT in a DDFFTT format, where DD is the wind direction in tens of degrees, FF is the wind velocity in knots
            and TT is the air temperature in deg C, rounded to the nearest integer and signed (e.g. TT = -16.85 deg C -> TT = -17)
            The DD and FF values are calculated in the following way :
               - the wind direction WD is converted in tens of degrees, and rounded to the nearest integer to obtain DD (e.g. WD = 247 deg -> 24.7 -> DD = 25)
               - if 100  UV  199 kts, then :
                    - the wind modulus UV is rounded to the nearest integer to obtain FF and :
                          DD = DD + 50
                          FF = FF - 100
               - if UV >  199, then :
                          FF = 99
               - if UV < 5, then :
                          DD = 99
                          FF = 00

          - If TT (temperature rounded to the nearest integer) is of 999 deg C, this indicates that the value is not available at that height, then the following values are assigned:
                          TT=99
                          DD=99
                          FF=99
            These values are only displayed for levels greater than 3000 feet. The condition mentioned previously on the writing of the forecasts at 3000 feet still applies.

          - There is no temperature forecast for the 3000 height (in feet) (e.g. DDFFTT becomes DDFF)

          - Truncation of the identification code of each station to conserve only the three last letters (e.g. CYUL becomes YUL)

          - In function of the forecast hours, production of a "backup" bulletin at the indicated hours by the "backupHour" key,
            with the addition of the appropriate line in the bulletin header.

          - Warning messages are sent if :
              - the forecast hour does not correspond to any of the planned output of the regular bulletin.
              - the wanted backup bulletin(s) correspond(s) to no planned bulletin of this type.

          - Transfer the bulletins and the backup bulletins, if available to the address indicated by the "outputPath" key

    Note : One day is added to the date of validity in the bulletin header if the hour of validity exceeds 24h

**Reference:**

-  For detailed information on the FDCN bulletins, consult the `Chapter
   3 <http://www.msc-smc.ec.gc.ca/msb/manuals/manair/pdf/french/chap3_f.pdf>`__
   of
   `MANAIR <http://www.msc-smc.ec.gc.ca/msb/manuals/manair/html/PDFMenu_f.cfm>`__.
   (link in French only)
-  Concerning the conversion of FDCN bulletins to FBCN format, consult
   `this
   document <https://wiki.cmc.ec.gc.ca/images/2/23/Spooki_-_Conversion_FD-FB.doc>`__.

**Keywords:**

-  IO, aviation, bulletin, vent/wind, température/temperature, FBCN,
   ASCII, station, backup, verticale/vertical

**Usage:**

**Call example:** ````

::

            ...
                spooki_run "[ReaderStd --input  $SPOOKI_DIR/pluginsRelatedStuff/WriterAsciiBulletinFB/testsFiles/inputFile.std] >>
                            [Select --verticalLevel 0.384@1.0] >>
                            [BulletinFBPreparation] >>
                            [WriterAsciiBulletinFB --outputPath /tmp/$USER]"

````

::

            ...
        

**Results validation:**

-  To come

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
   `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`WriterAsciiBulletinFB <WriterAsciiBulletinFB_8cpp.html>`__.

Units tests

`Evaluation tree <WriterAsciiBulletinFB_graph.png>`__

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
