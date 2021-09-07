English
-------

**Description:**

-  This slope index is the scalar product of the wind vector (at 850,
   700 or 500 hPa) and the topographic gradient.
-  Negative index indicates downslope effect. Positive index indicates
   upslope.
-  Useful for statistical spatial analysis.

\*Iteration method:\*

-  By point

\*Dependencies:\*

-  The wind components at 850, 700 or 500 hPa, UU and VV
   **and** one of the following fields:
-  Topographic elevation, ME
-  Geopotential height at surface, GZ

\*Result(s):\*

-  Slope index, SLX (m/s)

\*Algorithm:\*

.. code:: example

    #Relevant variables
    SLX = Slope Index (m/s)
    float ME = Topographic height (m)
    float UU = X component of wind (KTS)
    float VV = Y component of wind (KTS)
    int fetch = Number of grid point around central point i,j (default = 1)
    float dx = Distance between the two selected points in x (m)
    float dy = Distance between the two selected points in y (m)
    float A = 0.514444 = KTS -> m/s

    #Read UU and VV at 850, 700 or 500 (KTS)

    #Read ME or GZ at surface (m)

    #Calculation of Slope Index (m/s)

    For each point of the grid, we calculate the scalar product of the wind vector (at a certain uniform level) and topographic gradient.
    The topographic gradient is calculated in a centered manner, except for the points near the borders of a limited area grid
    where the gradient is calculated only in the quadrant of available points. If the user prefers to exclude these points, given that the
    the computation of the topographic gradient cannot be centered, the --excludeEdges option must be used and these grid points
    will have the value -999.

    If (i+fetch) && (i-fetch) && (j+fetch) && (j-fetch) exist
    dx = distance between points (i+fetch,j) and (i-fetch,j)
    dy = distance between points (i,j+fetch) and (i,j-fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj-fetch)/dy]

    Else If option --excludeEdges, return the value -999

    Else If (i-fetch) && (j-fetch) exist
    dx = distance between points (i,j) and (i-fetch,j)
    dy = distance between points (i,j) and (i,j-fetch)
    SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

    Else If (i+fetch) && (j+fetch) exist
    dx = distance between points (i,j) and (i+fetch,j)
    dy = distance between points (i,j) and (i,j+fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

    Else If (i+fetch) && (j-fetch) exist
    dx = distance between points (i,j) and (i+fetch,j)
    dy = distance between points (i,j) and (i,j-fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

    Else
    dx = distance between points (i,j) and (i-fetch,j)
    dy = distance between points (i,j) and (i,j+fetch)
    SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

**Reference:**

-  N/A

\*Keywords:\*

-  MÉTÉO/WEATHER, slope/pente, upslope, downslope

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SlopeIndex/testsFiles/inputFile.std] >>
                [SlopeIndex --fetch 2] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__
-  Coded by : `Guylaine Hardy, Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
