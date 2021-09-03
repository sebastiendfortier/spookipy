English
-------

**Description:**

-  Calculation of the thickness between two levels of a given
   geopotential height field.

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  A geopotential height field, GZ (at least 2 levels)

\*Result(s):\*

-  field DZ, with the same units as the source

\*Algorithm:\*

.. code:: example

    Verify that the type of vertical coordinate of the input field corresponds to the "coordinateType" key passed as parameter
    if true, get from the input field, with the help of the Select plug-in, the levels passed as parameters and do for each point:
        DZ = ABS ( GZ(top) - GZ(base) )
    else
        exit the plug-in with an error message
    end if

**Reference:**

-  Does not apply

\*Customizable condition:\*

-  ...

\*Keywords:\*

-  MÉTÉO/WEATHER, épaisseur/thickness, hauteur/height,
   géopotentielle/geopotential, niveau/level, différence/difference

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Thickness/testsFiles/inputFile.std] >>
                [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >>
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

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
