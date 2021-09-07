English
-------

**Description:**

-  Output the latitudes and longitudes for all grid points

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  One field of a grid

\*Result(s):\*

-  LA, latitude of each point of the given grid
-  LO, longitude of each point of the given grid

\*Algorithm:\*

    -  Call the appropriate EZSCINT functions
    -  Return latitudes and longitudes of the grid points

    \*References:\*

    -  `RMNLIB EZSCINT
       libraries <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

    \*Keywords:\*

    -  grille/grid, point, distance, latitude, longitude

    \*Usage:\*

    **Call example:**

    .. code:: example

        ...
        spooki_run "[ReaderStd         --input $SPOOKI_DIR/pluginsRelatedStuff/GridPointLatitudeLongitude/testsFiles/inputFile.std] >>
                    [GridPointLatitudeLongitude] >>
                    [WriterStd         --output /tmp/$USER/outputFile.std]"
        ...

    **Results validation:**

    **Contacts:**

    -  Author : `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Coded by : `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to

    Units tests

    | **Uses:**
    | **Used by:**

     
