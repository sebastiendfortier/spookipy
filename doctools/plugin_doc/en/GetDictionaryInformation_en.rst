English
-------

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

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  Does not apply

\*Result(s):\*

-  One or more fields containing the wanted information and having the
   name of the arguments of --outputAttribute key.
-  E.g. The selection of all the records of the "LATITUDE" attribute of
   the "MDICP4D" table of the "STATIONS.db" database will be a field
   having the name "LATITUDE".

\*Algorithm:\*

-  Make a SQL request on a given database and transfer the information
   received into one or more field(s)
-  Warning : the request can fail if a selected column in a table
   contains an empty record or if a string of characters contains a
   space.

\*Reference:\*

-  `SQLite <http://www.sqlite.org/>`__
-  `principle dictionary of meteorological
   stations <https://wiki.cmc.ec.gc.ca/wiki/Format_du_dictionnaire_de_stations_m%C3%A9t%C3%A9orologiques>`__
   (link currently in French only)

\*Keywords:\*

-  SYSTÈME/SYSTEM, base\ :sub:`dedonnées`/database,
   dictionnaire/dictionary, table

\*Usage:\*

.. code:: example

.. code:: example

**Call example:**

.. code:: example

    ...
    spooki_run "[GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table CANSTAT] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

-  `Other
   examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Examples_of_querying_a_database_with_SPOOKI>`__

\*Results validation:\*

-  ...

\*Contacts:\*

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
