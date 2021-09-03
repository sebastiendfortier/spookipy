English
-------

**Description:**

-  Calculate the occurrence of rime icing using the Appleman method.

\*Iteration method:\*

-  Column by column

\*Dependencies:\*

-  Air temperature (TT) °C
-  Dew point depression (ES) °C
-  Vertical motion (WW) en Pa/s.

\*Result(s):\*

-  Variable indicating the magnitude of rime icing.

\*Algorithm:\*

**Reference:**

-  `Appleman - Rime Icing
   Analysis <http://iweb/~afsypst/pluginsRelatedStuff/IcingRimeAppleman/Appleman-Rime-Analysis.pdf>`__

\*Keywords:\*

-  MÉTÉO/WEATHER, givre/icing, rime, appleman

\*Usage:\*

.. code:: example

    [IcingRimeAppleman --help]
          --help              Produce help message
          --verbose           Verbosity level
          --tlim arg          Temperature threshold
          --wlim arg          Vertical motion threshold
          --aplim arg         Standard deviation threshold

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/IcingRimeAppleman/testsFiles/inputFile.std] >>
                       [IcingRimeAppleman] >>
                       [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : George Karaganis
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
