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

-  reader

\*Usage:\*

.. code:: example

    [Reader --help]
      --help                  Produce help message
      --optimizationLevel arg Level of optimization, by default use global optimization level
      --verbose               Verbosity level
      --input arg             Filenames to be read. Each filename must be seperated by a comma.
      --forceReader arg       Force specific reader [ReaderStd|ReaderCsv]

**Call example:**

.. code:: example

    ...
    spooki_run "[Reader --input $SPOOKI_DIR/pluginsRelatedStuff/Reader/testsFiles/inputFile.std $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.csv] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
