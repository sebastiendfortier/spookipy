English
-------

**Description:**

-  Calculation of the pressure field for a given vertical coordinate.
-  The definition of the different coordinates are available in this
   `document. <https://wiki.cmc.ec.gc.ca/images/0/01/Spooki_-_Definitions_coordvert.pdf>`__
-  Possibility to calculate the pressure in the case of a `standard
   atmosphere <http://fr.wikipedia.org/wiki/Atmosph%C3%A8re_normalis%C3%A9eatmosphère%20normalisée>`__
   (constant pression ).
-  Others types of vertical coordinates could be added and documented in
   the future.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Any field on a set of given vertical levels

\*Result(s):\*

-  Pressure field PX (hPa or mb), on all the given levels

\*Algorithm:\*

-  https://wiki.cmc.ec.gc.ca/images/5/5c/Spooki_-_Algorithme_du_plugin_Pressure.pdf

\*Reference:\*

-  Inspired from the r.hy2pres utility of the RMNLIB library of RPN

\*Keywords:\*

-  MÉTÉO/WEATHER, pression/pressure, niveau/level,
   coordonnée/coordinate, r.hy2pres

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std] >>
                [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to .

Unit tests

| **Uses:**
| **Used by:**

 
