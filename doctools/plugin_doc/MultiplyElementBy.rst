=========================
Spooki: MultiplyElementBy
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

`MultiplyElementBy <classMultiplyElementBy.html>`__

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

`Français <../../spooki_french_doc/html/pluginMultiplyElementBy.html>`__

**Description:**

-  Multiplies each element of a field by a given value

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  A meteorological field

**Result(s):**

-  The meteorological field to which the given value has multiplied each
   element

**Algorithm:**

.. code-block:: text

            For F, a field of n elements

            For z, a value given by the "value" key

            for each point do

                F(n) = F(n) *  z        n >= 1

            end do

**Reference:**

-  Does not apply

**Keywords:**

-  UTILITAIRE/UTILITY, multiplier/multiply

**Usage:**

**Call example:** ````

::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std] >>
                        [MultiplyElementBy --value 10] >>
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

Reference to `MultiplyElementBy <classMultiplyElementBy.html>`__
:sup:``[code] <MultiplyElementBy_8cpp_source.html>`__`

Units tests

`Evaluation tree <MultiplyElementBy_graph.png>`__

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
