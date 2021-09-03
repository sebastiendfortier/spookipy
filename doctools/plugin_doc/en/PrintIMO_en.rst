English
-------

**Description:**

-  This plug-in is used for debugging and prints the content of the
   memory structure (IMO).

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  A field in the internal memory structure.

\*Result(s):\*

-  Does not apply

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  `Components of the internal memory
   structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components>`__

\*Keywords:\*

-  SYSTÈME/SYSTEM, impression/print, mémoire/memory, débogage/debugging

\*Usage:\*

.. code:: example

    [PrintIMO --help]
      --help                  Produce help message
      --optimizationLevel arg Level of optimization, by default use global optimization level
      --verbose               Verbosity level

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [PrintIMO  --output /tmp/$USER/outputFile.txt]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
