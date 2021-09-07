English
-------

**Description:**

-  Reading of standard file(s) and conversion into the system's internal
   memory structure.
-  The information associated to the spacial representation (also called
   "meta-information"), is read automatically and is conserved by
   default throughout the calculations.
-  `The variable
   dictionary <https://wiki.cmc.ec.gc.ca/wiki/Spooki/RelationsSpookiFSTD>`__
   is consulted during the reading of each variable and its
   corresponding unit is associated by default.
   \*/Note :/\*if two identical records are present in the input file,
   only the first will be kept

\*Iteration method:\*

-  Does not apply

\*Dependance:\*

-  One or more valid standard file(s) \*/Note :/\*The forecast hour is
   extracted with the help of the record descriptors DEET and NPAS and
   not directly from the record descriptor IP2

\*Result(s):\*

-  Standard files received from input converted into internal memory
   structure

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  `Documentation on standard
   files <https://wiki.cmc.ec.gc.ca/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI][Correspondence
   between the standard file record descriptors and the attributes of
   the internal memory of SPOOKI]]

\*Keywords:\*

-  IO, lecteur/reader, décodeur/decoder, standard , fichier/file

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ReaderStd_WriterStd/testsFiles/inputFile.std] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `ReaderStd <ReaderStd_8cpp.html>`__.

Units tests

| **Uses:**
| **Used by:**

 
