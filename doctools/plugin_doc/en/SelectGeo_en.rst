English
-------

**Description:**

-  ...

\*Iteration method:\*

-  ...

\*Dependencies:\*

-  ...

\*Result(s):\*

-  ...

\*Algorithm:\*

-  ...

\*Reference:\*

-  ...

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  sélection/selection, géographique/geographical, latitude, longitude

\*Usage:\*

.. code:: example

    [SelectGeo --help]
      --help                      Produce help message
      --optimizationLevel arg     Level of optimization, by default use global optimization level
      --verbose                   Verbosity level
      --latitude1 arg             Lower left corner latitude
      --longitude1 arg            Lower left corner longitude
      --latitude2 arg             Upper right corner latitude
      --longitude2 arg            Upper right corner longitude
      --xOffset arg               Offset along the x axis including first point
      --yOffset arg               Offset along the y axis including first point

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [SelectGeo --longitude1 272.425 --latitude1 45.1621 --longitude2 278.816 --latitude2 46.6413] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
