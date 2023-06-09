=========================
Spooki: VorticityAbsolute
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

`VorticityAbsolute <classVorticityAbsolute.html>`__

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

`Français <../../spooki_french_doc/html/pluginVorticityAbsolute.html>`__

**Description:**

-  Calculation of the absolute vorticity.

**Iteration method:**

-  Point by point

**Dependencies:**

-  Wind component along the X-axis of the grid, UU
-  Wind component along the Y-axis of the grid, VV

**Result(s):**

-  Absolute vorticity, QQ (1/s)

**Algorithm:**

    Call the `CoriolisParameter <classCoriolisParameter.html>`__ plug-in
    to obtain the Coriolis parameter, CORP (1/s).
    For UU (m/s) and VV (m/s), respectively the wind components along
    the X-axis and Y-axis.
    For \\(\\varphi\\) (radians), the latitude.
    Make a derivative off-center on a regional grid for the borders.
    Calculate the absolute vorticity, QQ (1/s), with the following
    formula:
    \\(\\mathrm{QQ\_{i,j} = ( VV\_{i+1,j} - VV\_{i-1,j} ) / ( X\_{i+1,j}
    - X\_{i-1,j} ) - ( UU\_{i,j+1} \* cos\\varphi\_{i,j+1} - UU\_{i,j-1}
    \* cos\\varphi\_{i,j-1} ) / ( ( Y\_{i,j+1} - Y\_{i,j-1} ) \*
    cos\\varphi\_{i,j} ) + CORP\_{i,j}}\\)

**Reference:**

-  "An Introduction to Dynamic Meteorology", Holton, James R.

**Keywords:**

-  MÉTÉO/WEATHER, vent/wind, tourbillon/vorticity, absolute/absolu,
   Coriolis

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VorticityAbsolute/testsFiles/inputFile.std] >>
                    [VorticityAbsolute] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Coded by : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `VorticityAbsolute <classVorticityAbsolute.html>`__
:sup:``[code] <VorticityAbsolute_8cpp_source.html>`__`

Unit tests

`Evaluation tree <VorticityAbsolute_graph.png>`__

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
