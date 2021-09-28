=========================
Spooki: GridPointDistance
=========================

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

`GridPointDistance <classGridPointDistance.html>`__

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

`Français <../../spooki_french_doc/html/pluginGridPointDistance.html>`__

**Description:**

-  Calculation of the distances on a horizontal grid between each point
   of which we know the latitude and longitude.
   The distance can be calculated in three different ways on each axis
   of the grid :

   -  centered distance    : for one given point, angular distance
      between the previous point and the next point
   -  forward distance      : for one given point, angular distance
      between the point and the next point
   -  backward distance   : for one given point, angular distance
      between the point and the previous point

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Grid of points (on at least one axis) of which we know the latitudes
   and longitudes respectively

**Result(s):**

-  The distances GDX (X axis) and GDY (Y axis) between each point of the
   given grid (meters)

**Algorithm:**

    For R, the mean radius of the Earth allowing to convert the angular
    distances GDX and GDY from radians to meters.
    For all the points i of latitude \\(\\lambda\\) (radians) and
    longitude \\(\\varphi\\) (radians), we use, depending on the value
    of the "differenceType" key,
    the appropriate trigonometric formula to calculate the angular
    distances :
    If axis = X then
       If differenceType = CENTERED then
            \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin
    \\lambda\_{i-1} \\cdot \\sin \\lambda\_{i+1} + \\cos \\varphi\_{i-1}
    \\cdot \\cos \\varphi\_{i+1} \\cdot \\cos (\\varphi\_{i+1} -
    \\varphi\_{i-1})]$}\\)
            For the 1st level:
                \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin
    \\lambda\_{i} \\cdot \\sin \\lambda\_{i+1} + \\cos \\varphi\_{i}
    \\cdot \\cos \\varphi\_{i+1} \\cdot \\cos (\\varphi\_{i+1} -
    \\varphi\_{i})]$}\\)
            For the last level:
                \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin
    \\lambda\_{i} \\cdot \\sin \\lambda\_{i-1} + \\cos \\varphi\_{i}
    \\cdot \\cos \\varphi\_{i-1} \\cdot \\cos (\\varphi\_{i} -
    \\varphi\_{i-1})]$}\\)
       Else if differenceType = FORWARD then
            \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin \\lambda\_{i}
    \\cdot \\sin \\lambda\_{i+1} + \\cos \\varphi\_{i} \\cdot \\cos
    \\varphi\_{i+1} \\cdot \\cos (\\varphi\_{i+1} - \\varphi\_{i})]$}\\)
            For the last level:
                \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin
    \\lambda\_{i} \\cdot \\sin \\lambda\_{i-1} + \\cos \\varphi\_{i}
    \\cdot \\cos \\varphi\_{i-1} \\cdot \\cos (\\varphi\_{i} -
    \\varphi\_{i-1})]$}\\)
       Else if differenceType = BACKWARD then
            \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin \\lambda\_{i}
    \\cdot \\sin \\lambda\_{i-1} + \\cos \\varphi\_{i} \\cdot \\cos
    \\varphi\_{i-1} \\cdot \\cos (\\varphi\_{i} - \\varphi\_{i-1})]$}\\)
            For the 1st level:
                \\(\\mbox{ $GDX\_{i} = R \\cdot \\arccos[\\sin
    \\lambda\_{i} \\cdot \\sin \\lambda\_{i+1} + \\cos \\varphi\_{i}
    \\cdot \\cos \\varphi\_{i+1} \\cdot \\cos (\\varphi\_{i+1} -
    \\varphi\_{i})]$}\\)
       End if
    Else if axis = Y then
       We proceed in the same way but with the points situated on the Y
    axis
    End if

***Note:*** The latitudes and longitudes must be in radians in the
trigonometric formula.
**References:**

-  `Great Circle <http://mathworld.wolfram.com/GreatCircle.html>`__

**Keywords:**

-  grille/grid, point, distance, centrée/centered, arrière/backward,
   avant/forward

**Usage:**

**Call example:** ````

::

     ...
     spooki_run "[ReaderStd         --input $SPOOKI_DIR/pluginsRelatedStuff/GridPointDistance/testsFiles/inputFile.std] >>
                 [GridPointDistance --axis X,Y --differenceType CENTERED] >>
                 [WriterStd         --output /tmp/$USER/outputFile.std]"
     ...
     

**Results validation:**

**Contacts:**

-  Author : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `GridPointDistance <classGridPointDistance.html>`__
:sup:``[code] <GridPointDistance_8cpp_source.html>`__`

Units tests

`Evaluation tree <GridPointDistance_graph.png>`__

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
