English
-------

**Description:**

-  Search of occurrence(s) in the vertical of the A=B event, where A is
   from a reference field and B is from a comparison field. Depending on
   the user's request, the plug-in calculates for each occurrence, the
   geopotential height and/or the pressure associated by linear
   interpolation in the cases where A=B between 2 given levels
   (interpolation in ln(p) if the requested output is in pressure).
   Besides, if A=B on the 1st level of the sample, the plug-in does not
   consider this level and continues its search starting with the
   following level.
-  A boolean variable BOVS is created to give an indication of the
   comparative value of A in respect to B at the 1st level of the
   sample. More specifically, BOVS=false (0) if A < B at the lowest
   level, and BOVS=true (1) inversely. In the case where A=B at the 1st
   level, it is the following level that will be able to decide the
   value of the logical variable: if the following level is such that A
   < B then BOVS=false (0), and BOVS=true (1) inversely. In the case
   where A=B on many consecutive levels starting from the lowest level
   of the sample, the plug-in searches for the 1st level where A is
   different from B and returns BOVS=false (0) if A < B at this level,
   and BOVS=true (1) inversely.
-  A boolean variable BOEQ is also created if the option
   --checkForEquality is used. This option is used to verify if A = B at
   the first level. BOEQ=false (0) if A != B at the first level, and
   BOEQ=true (1) if A = B.
-  For example, if we search for the occurrences of the T=0 event where
   T is the temperature of the environment (reference field) and 0 is
   the 0 degC isotherm (comparison field), the plug-in will indicate
   BOVS=false (0) if T < 0 at the surface and true (1), if T > 0. Other
   examples of the plug-in's use : search for cloudy layers, icing, warm
   and/or cold layers, positive energy zones (CAPE).

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  Geopotential height GZ an/or pressure PX, depending on the user's
   choice
-  A reference field
-  A comparison field or value (depending on the *comparisonType* key)

\*Result(s):\*

-  Geopotential height (dam) an/or height in pressure (mb) associated
   with the occurrences of the A=B event, AGZ and APX respectively
   (these are fields where the vertical dimension corresponds to the
   maximum number of occurrences requested by the user)
-  Boolean variable, BOVS (2D)
-  Number of occurrences of the A=B event, NBVS (2D)
   **If** the option checkForEquality is used:
-  Boolean variable, BOEQ (2D)

\*Algorithm:\*

-  `https://wiki.cmc.ec.gc.ca/images/1/17/Spooki_-_VerticalScan_Algorithm.odt <https://wiki.cmc.ec.gc.ca//images/1/17/Spooki_-_VerticalScan_Algorithm.odt>`__
-  `https://wiki.cmc.ec.gc.ca/images/6/6d/Spooki_-_VerticalScan_Algorithm.pdf <https://wiki.cmc.ec.gc.ca//images/6/6d/Spooki_-_VerticalScan_Algorithm.pdf>`__

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITY/UTILITAIRE, search/recherche, scan/balayage, occurrence,
   level/niveau, vertical

\*Usage:\*

    For the --comparisonType key:

    -  CONSTANTVALUE: Compare each column of the reference field to the
       same constant value
    -  VARIABLEVALUE: Compare each column of the reference with the
       horizontally collocated value given by the 2D comparison field
    -  INTERSECTIONS: Compare the collocated columns of the 3D reference
       field and the 3D comparison field to find where they intersect in
       the vertical For the --comparisonValueOrField key:
    -  Requires a value for: --comparisonType CONSTANTVALUE
    -  Requires the name of a 2D field with the same horizontal coverage
       as the reference field for: --comparisonType VARIABLEVALUE
    -  Requires the name of a 3D field collocated with the reference
       field for: --comparisonType INTERSECTIONS
       **Notes :**
       This plugin can be executed in various contexts :
    -  We can search for a constant on the whole column (e.g. searching
       for freezing levels, where we search for the occurrences of TT =
       0 deg C).
    -  We can search for an occurrence on the whole column or only on a
       sample of the column.
    -  The plug-in can receive a 3D field or just a vertical profile
       from input

    \*Call example:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VerticalScan/testsFiles/inputFile.std] >>
                    [VerticalScan --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --maxNbOccurrence 5 --epsilon 0.000001] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Results validation:**

    **Contacts:**

    -  Auteur(e) : `Sandrine
       Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
    -  Codé par : `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__,
       Jonathan Cameron, `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to

    Units tests

    | **Uses:**
    | **Used by:**

     
