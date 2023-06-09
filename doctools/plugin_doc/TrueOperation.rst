=====================
Spooki: TrueOperation
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

`TrueOperation <classTrueOperation.html>`__

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

`Francais <../../spooki_french_doc/html/pluginTrueOperation.html>`__

**Description:**

-  Logical operation that always returns true.

**Iteration method:**

-  Does not apply

**Dependencies:**

-  None

**Result(s):**

-  Returns true to the system (operational system)
   ***Note:*** No data is outputted from the plug-in

**Algorithm:**

-  Does not apply

**Reference:**

-  Does not apply

**Keywords:**

-  SYSTÈME/SYSTEM, logique/logical, vrai/true

**Usage:**

::

        [TrueOperation --help]
          --help                  Produce help message
          --optimizationLevel arg Level of optimization, by default use global optimization level
          --verbose               Verbosity level

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                    ( [TrueOperation] + [Copy] || [FalseOperation] ) >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

-  ...

**Contacts:**

-  Author : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `TrueOperation <classTrueOperation.html>`__
:sup:``[code] <TrueOperation_8cpp_source.html>`__`

`Evaluation tree <TrueOperation_graph.png>`__

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
