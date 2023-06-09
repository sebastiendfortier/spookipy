================
Spooki: ZapSmart
================

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

`ZapSmart <classZapSmart.html>`__

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

`Francais <../../spooki_french_doc/html/pluginZapSmart.html>`__

**Description:**

-  Allows to select and rename one or more value(s) of field
   attribute(s) in the internal memory structure.
-  The parameter keys are declared in pairs in the form of : from -> to

**Iteration method:**

-  Does not apply

**Dependencies:**

-  At least one attribute of the internal memory structure

**Result(s):**

-  One or more field(s) which the attribute value(s) is(are) selected
   and renamed in accordance with the arguments given to the parameter
   keys

**Algorithm:**

-  Selects one or more attribute(s) of the field in the memory structure
   with the help of the `Select <classSelect.html>`__ plug-in
-  Modifies the attribute value(s) with the help of the
   `Zap <classZap.html>`__ plug-in
-  Selects the other attributes of the field with the help of the
   `Select <classSelect.html>`__ plug-in and the "exclude" parameter key
   to keep them intact

**Reference:**

-  `Components of the internal memory
   structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components#meteo_infos:>`__
-  `Correspondence between the recording descriptors of standard files
   and the attributes of the internal memory of
   SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI>`__

**Keywords:**

-  SYSTÈME/SYSTEM, zap, renommer/rename

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ZapSmart/testsFiles/inputFile.std] >>
                    [ZapSmart --fieldNameFrom VV --fieldNameTo UU] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

-  ...

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `ZapSmart <classZapSmart.html>`__
:sup:``[code] <ZapSmart_8cpp_source.html>`__`

Tests unitaires

`Evaluation tree <ZapSmart_graph.png>`__

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
