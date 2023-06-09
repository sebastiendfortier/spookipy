========================
Spooki: GridMergeSimilar
========================

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

`GridMergeSimilar <classGridMergeSimilar.html>`__

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

`Francais <../../spooki_french_doc/html/pluginGridMergeSimilar.html>`__

**Description:**

-  Merging of all the similar grids received by the plug-in.
-  Grids are similar when their projection type and their size along X
   and along Y are identical.
-  If at least one grid is not similar to the other available grids, the
   plug-in fails.

**Iteration method:**

-  Does not apply

**Dependencies:**

-  At least one field from input

**Result(s):**

-  All the fields on a single grid

**Algorithm:**

-  Does not apply

**Reference:**

-  None

**Keywords:**

-  UTILITAIRE/UTILITY, grille/grid, similaire/similar, merge/fusion

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/GridMergeSimilar/testsFiles/inputFile.std] >>
                    [GetDictionaryInformation --dataBase STATIONS --table STATIONSFB --outputAttribute FictiveStationFlag ] >>
                    [GridMergeSimilar] >> [PrintIMO]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `GridMergeSimilar <classGridMergeSimilar.html>`__
:sup:``[code] <GridMergeSimilar_8cpp_source.html>`__`

Units tests

`Evaluation tree <GridMergeSimilar_graph.png>`__

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
