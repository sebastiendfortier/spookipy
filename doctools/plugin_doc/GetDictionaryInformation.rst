================================
Spooki: GetDictionaryInformation
================================

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

`GetDictionaryInformation <classGetDictionaryInformation.html>`__

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

`Francais <../../spooki_french_doc/html/pluginGetDictionaryInformation.html>`__

**Description:**

-  Reading of the dictionaries used in the SPOOKI system.
-  Each database is constructed of one or more table(s), which
   contain(s) several attributes, that, in turn, contain several
   records.
-  The content of the available database can be consulted here (link to
   the Doxygen page "List of the databases" of the domain used: beta,
   development,...).
-  This plug-in allows to select the attributes of one or more table(s)
   of a same specified database.
-  Possibility to use a simple request corresponding to the use of the
   "WHERE" clause of the SQlite language, as well as an advanced request
   corresponding to a direct SQlite command based on the "SELECT FROM
   WHERE" expression.
-  Usage examples of this plug-in are available
   **`here <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Examples_of_querying_a_database_with_SPOOKI>`__**
   ***Note:*** Pour le moment, seules les tables EXTRASSTATIONS,
   EXTRASSTATIONSRAW, MDICP4D, MDICP4DRAW, PRODUCTS et STATIONSFB de la
   base de données STATIONS.db peuvent être consultées sans risque.

**Iteration method:**

-  Does not apply

**Dependencies:**

-  Does not apply

**Result(s):**

-  One or more fields containing the wanted information and having the
   name of the arguments of –outputAttribute key.
-  E.g. The selection of all the records of the "LATITUDE" attribute of
   the "MDICP4D" table of the "STATIONS.db" database will be a field
   having the name "LATITUDE".

**Algorithm:**

-  Make a SQL request on a given database and transfer the information
   received into one or more field(s)
-  Warning : the request can fail if a selected column in a table
   contains an empty record or if a string of characters contains a
   space.

**Reference:**

-  `SQLite <http://www.sqlite.org/>`__
-  `principle dictionary of meteorological
   stations <https://wiki.cmc.ec.gc.ca/wiki/Format_du_dictionnaire_de_stations_m%C3%A9t%C3%A9orologiques>`__
   (link currently in French only)

**Keywords:**

-  SYSTÈME/SYSTEM, base\_de\_données/database, dictionnaire/dictionary,
   table

**Usage:**

::

::

**Call example:** ````

::

        ...
        spooki_run "[GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table CANSTAT] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

-  `Other
   examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Examples_of_querying_a_database_with_SPOOKI>`__

**Results validation:**

-  ...

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`GetDictionaryInformation <classGetDictionaryInformation.html>`__
:sup:``[code] <GetDictionaryInformation_8cpp_source.html>`__`

Tests unitaires

`Evaluation tree <GetDictionaryInformation_graph.png>`__

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
