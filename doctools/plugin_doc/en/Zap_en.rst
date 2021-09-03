English
-------

**Description:**

-  Allows to rename one or more value(s) of field attribute(s) in the
   internal memory structure of the system, without affecting the data
   itself.
   ***Note:*** the arguments given to the parameter keys correspond to
   the new values of the attributes

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one field in the internal memory structure

\*Result(s):\*

-  One or more field(s) which the attribute value(s) are renamed in
   accordance with the arguments given to the parameter keys

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  `Components of the internal memory
   structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI][Correspondence
   between the recording descriptors of standard files and the
   attributes of the internal memory of SPOOKI]]

\*Keywords:\*

-  SYSTÈME/SYSTEM, zap, renommer/rename

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Zap/testsFiles/inputFile.std] >>
                [Select --fieldName UU] >>
                [Zap --fieldName FF --pdsLabel WINDMODULUS --typeOfField ANALYSIS --dateOfOrigin 20080529133415
                --forecastHour 144 --userDefinedIndex 66 --unit scalar] >>
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

Tests unitaires

| **Uses:**
| **Used by:**

 
