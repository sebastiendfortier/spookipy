English
-------

**Description:**

-  

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one field in the internal memory structure

\*Result(s):\*

-  One field

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  `Components of the internal memory
   structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI][Correspondence
   between the recording descriptors of standard files and the
   attributes of the internal memory of SPOOKI]]

\*Keywords:\*

-  SYSTÈME/SYSTEM, calculator, renommer/rename

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Calculator/testsFiles/srcFile2.std] >>
                [Select --fieldName TT ] >> [Zap --tag tt] >> [Calculator --expression *7 --unit celsius --outputFieldName RSLT] >>
                [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
