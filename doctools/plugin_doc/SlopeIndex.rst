==================
Spooki: SlopeIndex
==================

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

`SlopeIndex <classSlopeIndex.html>`__

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

`Français <../../spooki_french_doc/html/pluginSlopeIndex.html>`__

**Description:**

-  This slope index is the scalar product of the wind vector (at 850,
   700 or 500 hPa) and the topographic gradient.
-  Negative index indicates downslope effect. Positive index indicates
   upslope.
-  Useful for statistical spatial analysis.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  The wind components at 850, 700 or 500 hPa, UU and VV

| **and** one of the following fields:

-  Topographic elevation, ME
-  Geopotential height at surface, GZ

**Result(s):**

-  Slope index, SLX (m/s)

**Algorithm:**

.. code:: fragment

        SLX       = Slope Index (m/s)
        float ME  = Topographic height (m)
        float GZ  = Geopotential height (dam)
        float UU  = X component of wind (KTS)
        float VV  = Y component of wind (KTS)
        int fetch = Number of grid point around central point i,j (default = 1)
        float dx  = Distance between the two selected points in x (m)
        float dy  = Distance between the two selected points in y (m)
        float A   = 0.514444 = KTS -> m/s

        If ME is absent
            Read GZ surface
            Convert to meters
            Zap to ME
        End if

        For each point of the grid, we calculate the scalar product of the wind vector (at a certain uniform level) and topographic gradient.
        The topographic gradient is calculated in a centered manner, except for the points near the borders of a limited area grid
        where the gradient is calculated only in the quadrant of available points. If the user prefers to exclude these points, given that the
        the computation of the topographic gradient cannot be centered, the --excludeEdges option must be used and these grid points
        will have the value -999.

        If (i+fetch) && (i-fetch) && (j+fetch) && (j-fetch) exist
            dx = distance between points (i+fetch,j) and (i-fetch,j)
            dy = distance between points (i,j+fetch) and (i,j-fetch)
            SLXi,j = A*UUi*[(MEi+fetch-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj-fetch)/dy]

        Else 

            If option --excludeEdges 
                SLXi,j = -999

            Else if (i-fetch) && (j-fetch) exist
                dx = distance between points (i,j) and (i-fetch,j)
                dy = distance between points (i,j) and (i,j-fetch)
                SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

             Else if (i+fetch) && (j+fetch) exist
                dx = distance between points (i,j) and (i+fetch,j)
                dy = distance between points (i,j) and (i,j+fetch)
                SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

            Else if (i+fetch) && (j-fetch) exist
                dx = distance between points (i,j) and (i+fetch,j)
                dy = distance between points (i,j) and (i,j-fetch)
                SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

            Else
                dx = distance between points (i,j) and (i-fetch,j)
                dy = distance between points (i,j) and (i,j+fetch)
                SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

            End if
        End if

**Reference:**

-  N/A

**Keywords:**

-  MÉTÉO/WEATHER, slope/pente, upslope, downslope

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SlopeIndex/testsFiles/inputFile.std] >>
                    [SlopeIndex --fetch 2] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__
-  Coded by : `Guylaine
   Hardy, <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__ `Sébastien
   Fortier, Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `SlopeIndex <classSlopeIndex.html>`__
:sup:``[code] <SlopeIndex_8cpp_source.html>`__`

Units tests

`Evaluation tree <SlopeIndex_graph.png>`__

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
