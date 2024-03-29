=====================
Spooki: FilterDigital
=====================

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

`FilterDigital <classFilterDigital.html>`__

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

`Francais <../../spooki_french_doc/html/pluginFilterDigital.html>`__

**Description:**

-  Apply a digital filter of Stencil type on a data set.
-  The filter, applied on one given point, in one direction of the given
   field, is characterized by a list of weights (odd number) symmetrical
   to the considered point and to the number of times it is applied.
-  The filter is applied successively in each direction of the given
   field.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  A meteorological field on a grid.

**Result(s):**

-  The filtered values of the meteorological field.

**Algorithm:**

    For F, a given field of components F(i), in the direction NI
    (i=1,NI).

    For \\(\\mbox{ $w\_n$}\\), (n=1,N), a list of N weights associated
    to the digital filter applied on the F field, which the result
    \\(\\mbox{ $F^\*$}\\) on each component is expressed as :

    \\(\\mbox{ $F^\*(i) = \\frac {\\sum\_{n=1}^{N} w\_n F(i -
    {\\scriptstyle[\\frac{N+1}{2}- n]})}{\\sum\_{n=1}^{N} w\_n}$}\\)    
    \\(\\mbox{ $, 2 \\leq i \\leq NI-1$}\\)

    This operation is repeated ("repetitions" key), in the direction NI,
    as many times as the specified number in parameter.

    We proceed in the same way in each direction of the F field,
    successively.

    ***Note:*** : in the case of a 2D field, the algorithm is first
    applied in the direction NI, and then in the direction NJ.

**Reference:**

-  `Inspired from the FILTRE function (stenfilt.f) of the PGSM
   utility <https://wiki.cmc.ec.gc.ca/w/images/d/dc/Spooki_-_Filtre_html.pdf>`__

**Keywords:**

-  UTILITAIRE/UTILITY, filtre/filter, digital, stencil

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/FilterDigital/testsFiles/inputFile.std] >>
                    [FilterDigital --filter 1,2,1 --repetitions 2] >>
                    [WriterStd     --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `FilterDigital <classFilterDigital.html>`__
:sup:``[code] <FilterDigital_8cpp_source.html>`__`

Units tests

`Evaluation tree <FilterDigital_graph.png>`__

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
