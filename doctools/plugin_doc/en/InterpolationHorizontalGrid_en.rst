English
-------

**Description:**

-  voir
   `c\ :sub:`ezsint` <http://web-mrb.cmc.ec.gc.ca/mrb/si/eng/si/libraries/rmnlib/ezscint/>`__

\*Iteration method:\*

-  N/A

\*Dependencies:\*

-  N/A

\*Result(s):\*

-  N/A

\*Algorithm:\*

-  N/A

\*References:\*

-  `Grid types supported by RPN Standard
   Files <http://web-mrb.cmc.ec.gc.ca/science/si/eng/si/misc/grilles.html>`__

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  interpolateur/interpolator, interpolation,
   extrapolateur/extrapolator, extrapolation, horizontale/horizontal

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalGrid/testsFiles/inputFile.std] >>
                [InterpolationHorizontalGrid --outputGridDefinitionMethod USER_DEFINED
                                                --gridType TYPE_N
                                                --xyDimensions 191,141
                                                --gridProjectionParameters 79.0,117.0,57150.0,21.0
                                                --interpolationType BI-LINEAR
                                                --extrapolationType VALUE=99.9] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

-  `Other
   examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Example_of_horizontal_interpolation>`__

\*Results validation:\*

-  Under construction!

\*Contacts:\*

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
