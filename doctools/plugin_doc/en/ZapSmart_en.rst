English
-------

**Description:**

-  Allows to select and rename one or more value(s) of field
   attribute(s) in the internal memory structure.
-  The parameter keys are declared in pairs in the form of : from -> to

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one attribute of the internal memory structure

\*Result(s):\*

-  One or more field(s) which the attribute value(s) is(are) selected
   and renamed in accordance with the arguments given to the parameter
   keys

\*Algorithm:\*

-  Selects one or more attribute(s) of the field in the memory structure
   with the help of the plug-in
-  Modifies the attribute value(s) with the help of the plug-in
-  Selects the other attributes of the field with the help of the
   plug-in and the "exclude" parameter key to keep them intact

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
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ZapSmart/testsFiles/inputFile.std] >>
                [ZapSmart --fieldNameFrom VV --fieldNameTo UU] >>
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

Tests unitaires

| **Uses:**
| **Used by:**

 
