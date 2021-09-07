English
-------

**Description:**

-  Logical operation that always returns true.

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  None

\*Result(s):\*

-  Returns true to the system (operational system)
   ***Note:*** No data is outputted from the plug-in

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  SYSTÈME/SYSTEM, logique/logical, vrai/true

\*Usage:\*

.. code:: example

    [TrueOperation --help]
      --help                  Produce help message
      --optimizationLevel arg Level of optimization, by default use global optimization level
      --verbose               Verbosity level

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                ( [TrueOperation] + [Copy] || [FalseOperation] ) >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
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

| **Uses:**
| **Used by:**

 
