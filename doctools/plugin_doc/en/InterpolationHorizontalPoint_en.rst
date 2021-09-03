English
-------

**Description:**

**Iteration method:**

-  N/A

\*Dependencies:\*

-  N/A

\*Result(s):\*

-  N/A

\*Algorithm:\*

-  N/A

\*References:\*

-  N/A

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  

   -  INTERPOLATION, extrapolation, horizontale/horizontal, point,
      ezscint

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.std] >>
                [ReaderCsv --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.csv] >>
                [InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  Under construction!

\*Contacts:\*

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
