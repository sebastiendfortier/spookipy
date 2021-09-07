English
-------

**Description:**

-  Displays a given message in the standard output (STDOUT) during the
   execution

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  None

\*Result(s):\*

-  The message is displayed in the standard output (STDOUT).
   ***Note:*** No data is outputted from this plug-in.

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  SYSTÈME/SYSTEM, message, STDOUT

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Message/testsFiles/inputFile.std] >>
                ( [Select --fieldName TT] || ([Copy] + [Message --severity WARNING --verificationMessage No_TT_found,_write_anyway]) ) >>
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

 
