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

-  graphique/graphic, carte/map, writer

\*Usage:\*

.. code:: example

.. code:: example


**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/GraphicWriter/testsFiles/4panneaux/12h/inputFile.std] >>
                [QuatrePanneaux --forecastHour 12 --hourDelta 12 --jobName R1DFX03 --runId R1 --runHour 00] >>
                [WriterGraphic --intermediateDataFilename /tmp/4p.std --tool SIGMA --addNoiseForHighLow --output /tmp/$USER/outputFile.rrbx]"
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

 
