=========================
Spooki: IcingRimeAppleman
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

`IcingRimeAppleman <classIcingRimeAppleman.html>`__

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

`Français <../../spooki_french_doc/html/pluginIcingRimeAppleman.html>`__

**Description:**

-  Calculate the occurrence of rime icing using the Appleman method.

**Iteration method:**

-  Column by column

**Dependencies:**

-  Air temperature (TT) °C
-  Dew point depression (ES) °C
-  Vertical motion (WW) en Pa/s.

**Result(s):**

-  Variable indicating the magnitude of rime icing.

**Algorithm:**

**Reference:**

-  `Appleman - Rime Icing
   Analysis <http://iweb/~afsypst/pluginsRelatedStuff/IcingRimeAppleman/Appleman-Rime-Analysis.pdf>`__

**Keywords:**

-  MÉTÉO/WEATHER, givre/icing, rime, appleman

**Usage:**

::

         [IcingRimeAppleman --help]
               --help              Produce help message
               --verbose           Verbosity level
               --tlim arg          Temperature threshold
               --wlim arg          Vertical motion threshold
               --aplim arg         Standard deviation threshold

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/IcingRimeAppleman/testsFiles/inputFile.std] >>
                           [IcingRimeAppleman] >>
                           [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

-  ...

**Contacts:**

-  Author : George Karaganis
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `IcingRimeAppleman <classIcingRimeAppleman.html>`__
:sup:``[code] <IcingRimeAppleman_8cpp_source.html>`__`

Units tests

`Evaluation tree <IcingRimeAppleman_graph.png>`__

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
