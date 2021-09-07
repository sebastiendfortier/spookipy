English
-------

**Description:**

-  Logical operation that always returns false

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  None

\*Result(s):\*

-  Returns false to the system (operational system) and stops the
   execution of the program.
   ***Note:*** No data is outputted from this plug-in

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  SYSTÈME/SYSTEM, logique/logical, faux/false

\*Usage:\*

.. code:: example

    [FalseOperation --help]
      --help                  Produce help message
      --optimizationLevel arg Level of optimization, by default use global optimization level
      --verbose               Verbosity level
      --version               Get version number

.. code:: example


**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std] >>
                ( [Copy] || [FalseOperation] ) >>
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

 
