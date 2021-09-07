English
-------

**Description:**

-  one or more field(s) in the internal memory structure, depending on
   one or more argument(s) passed to the parameter keys.
-  NOTE: in the case of field(s) extracted from standard files, all the
   meta-information is automatically selected with all selection of
   field(s) (unless if one of the optional --noMetadata or
   --metadataFieldName parameter keys is specified)

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least one field in the internal memory structure

\*Result(s):\*

-  One or more selected field(s) depending on the arguments passed to
   the parameter keys

\*Algorithm:\*

-  Index, with the help of a database, the records depending on the
   selection criteria
-  with the help of the appropriate index(es)
-  Return the result

\*Reference:\*

-  `Components of the internal memory
   structure <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/System_components#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI][Correspondence
   between the standard file descriptors of the records and the
   attributes of the internal memory of SPOOKI]]

\*Keywords:\*

-  SYSTÈME/SYSTEM, sélection/selection

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Select/testsFiles/inputFile.std] >>
                [Select    --fieldName UU] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__, `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
