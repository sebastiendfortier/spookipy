English
-------

**Description:**

Cuts a piece out of a grid, defined by its upper left hand corner and
lower right hand corner.

    \*/\ Notes:/*

    -  This plug-in allows for the creation of a completely autonomous
       grid.
    -  If one desires to merge several grids, these grids must have been
       cut by this plug-in in the same SPOOKI execution.

    \*Iteration method:\*

    -  Point by point.

    \*Dependencies:\*

    -  One or several field(s) on one or several input grid(s).

    \*Result(s):\*

    -  The input fields on a piece of the grid, with the same input
       metadata.

    \*Algorithm:\*

    -  The input grids are referenced, as well as their data and their
       descriptors.
    -  The output grids are created by copying the input grid parameters
       and by modifying the dimensions.
    -  The desired data is copied.

    \*Reference:\*

    -  N/A

    \*Keywords:\*

    -  SYSTÈME/SYSTEM, grille/grid, découpage/cut, sélection/select

    \*Usage:\*

    .. code:: example

        [GridCut --help]
        --help                      Produce help message
        --optimizationLevel arg     Level of optimization, by default use global optimization level
        --verbose                   Verbosity level
        --startPoint arg            The upper left point of the matrix
        --endPoint arg              The lower right poinr of the matrix

    **Call example:**

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/GridCut/testsFiles/inputFile.std] >>
        [GridCut --startPoint 5,16 --endPoint 73,42] >>
        [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Results validation:**

    **Contacts:**

    -  Author : `Maximilien
       Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__
    -  Coded by : `Maximilien
       Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to

    Units tests

    | **Uses:**
    | **Used by:**

     
