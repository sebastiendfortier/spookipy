========================
Spooki: SetLowerBoundary
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

`SetLowerBoundary <classSetLowerBoundary.html>`__

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

`Français <../../spooki_french_doc/html/pluginSetLowerBoundary.html>`__

**Description:**

-  Limit the minimum of a field to the specified value

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  A meteorological field

**Result(s):**

-  The meteorological field of which no value is less than the specified
   value

**Algorithm:**

.. code-block:: text

        For F, a given field of size N, composed of n elements (n = 1,N)

        For z, a value given by the "value" key, designated as the lower boundary of the field F

        For each point n=1,N do

            If F(n) < z then
               F(n) = z
            End if

        End do

**Reference:**

-  Does not apply

**Keywords:**

-  UTILITAIRE/UTILITY, minimum, borne/bound, inférieur/lower

**Usage:** htmlonly<iframe id="usage"
src="forward2python.php/spooki\_create\_dynamic\_doc\_parts/usage/SetLowerBoundary"
width="100%" frameborder="0" scrolling="no"
onload="resizeFrame(document.getElementById('usage'))"></iframe>

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetLowerBoundary/testsFiles/inputFile.std] >>
                    [SetLowerBoundary --value 1 ] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `SetLowerBoundary <classSetLowerBoundary.html>`__
:sup:``[code] <SetLowerBoundary_8cpp_source.html>`__`

Units tests

`Evaluation tree <SetLowerBoundary_graph.png>`__

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
