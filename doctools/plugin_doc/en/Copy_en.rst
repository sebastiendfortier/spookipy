English
-------

**Description:**

-  Copies the input field without modification

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one input field.

\*Result(s):\*

-  The same input field

\*Algorithm:\*

-  A[i,j,k] = A[i,j,k]

\*Reference:\*

-  None

\*Keywords:\*

-  SYSTÈME/SYSTEM, copie/copy, logique/logical

\*Usage:\*

.. code:: example

    [Copy --help]
      --help                    Produce help message
      --optimizationLevel arg   Level of optimization, by default use global optimization level
      --verbose                 Verbosity level
      --version                 Version number

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Copy/testsFiles/inputFile.std] >>
                ( [Copy] + [Message --severity WARNING --verificationMessage copy_of_input] ) >>
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

| **Uses:**
| **Used by:**

 
