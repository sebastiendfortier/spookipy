English
-------

**Description:**

-  Writing data into a file in RPN standard format
-  Convert, by default, each variable to the unity corresponding to the
   `standard variables
   dictionary <http://iweb/~afsypst/spooki/spooki_french_doc/html/stdvar.html>`__.

\*Iteration method:\*

-  Does not apply

\*Dependance:\*

-  Data in the internal memory of the SPOOKI system (PDS)

\*Result(s):\*

-  One or more encoded record(s) in a file of RPN standard format
-  The records are sorted and written in the following order :
   meta-informations, names of the variables in alphabetic order, level
   order (from bottom to top), temporal order

\*Algorithm:\*

-  With the help of the table on the correspondence between the
   `standard files and
   SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI>`__,
   this plug-in transfers (writes) the information of the attributes
   from the internal memory of SPOOKI to the record descriptors of the
   standard files by following `theses
   rules <https://wiki.cmc.ec.gc.ca/index.php?title=Spooki/en/Table_of_rules_for_WriterStd&action=edit&redlink=1>`__.
-  Convert each variable to its standard unit designated by the
   `standard variables
   dictionary <http://iweb/~afsypst/spooki/spooki_french_doc/html/stdvar.html>`__,
   with the help of the plug-in, unless the "--noUnitConversion" key is
   activated. During this conversion, the second character of TYPVAR is
   not affected. If the original unit is unknown, the conversion cannot
   be done, the plug-in stops by indicating: "The unit is unknown, if
   you wish to write the variable with the original unit, use the
   &ndash;noUnitConversion key."
-  Sort the variables in the order designated by the system
   (meta-informations, names of the variables in alphabetic order, level
   order (from bottom to top), temporal order).
-  If the "--noMetadata" key is activated, do not copy the
   "meta-informations" (information associated to the spacial
   representation: ">>","^^","HY","P0","PT","E1","!!","!!SF" records).
-  If the "--metadataOnly" key is activated, only copy the
   "meta-informations" (information associated to the spacial
   representation: ">>","^^","HY","P0","PT","E1","!!","!!SF" records).
-  This plug-in writes to the file named by the argument given to the
   "--output" key. If this file already exists, by default
   (APPENDOVERWRITE option of the "--writingMode" key), we write over
   the records that have the same values in the record descriptors as
   the new data and we keep the other data that is already in the file.
   If we choose the NOPREVIOUS option of the "--writingMode" key and the
   file already exists, the plug-in stops with an appropriate message.
   If we chose the NEWFILEONLY option, we erase the file and we create a
   new file containing exclusively the new data. **Important**: If the
   file (in the --output argument) already exists and this file is not a
   standard file, the request stops by indicating that the file in the
   --output argument already exists and is not of standard type. We then
   invite the user to resolve the conflict before relaunching SPOOKI.
-  The final file does not contain two distinct fields of "HY" or of
   "!!". For the "^^" and ">>", the distinct fields are allowed unless
   they have the same IP1 and IP2 but not the same IG1,IG2,IG3 and IG4.
   If a second distinct "HY" or "!!" or disallowed distinct "^^" and
   ">>" fields exist in the data to be written and/or in the writing
   file, the request stops with a clear message explaining the problem.

\*Reference:\*

-  `Documentation on standard
   files <https://wiki.cmc.ec.gc.ca/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
-  `Table of comparison between the standard file and
   SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Correspondence_STD_Files_-_SPOOKI>`__

\*Keywords:\*

-  IO, standard, graveur/writer, fichier/file

\*Usage:\*

    | ***Notes: For the "--writingMode" key:***

    -  NOPREVIOUS: The plug-in stops if the standard file already
       exists.
    -  APPEND : If the standard file already exists, we add all the
       records into the available memory of the plug-in.
    -  APPENDNEW: If the standard file already exists, we only add the
       records that do not have the same values in the record
       descriptors as those already present in the file. (This option
       will be implemented later.)
    -  APPENDOVERWRITE: If the standard file already exists, we write
       over the records that have the same values in the record
       descriptors as the new data and we keep the other data that is
       already in the file. (default mode)
    -  NEWFILEONLY: If the standard file already exists, we erase the
       file and we create a new file containing exclusively the new
       data.

    \*Call example:\*

    .. code:: example

        ...
            spooki_run "[ReaderStd --input  $SPOOKI_DIR/pluginsRelatedStuff/ReaderStd_WriterStd/testsFiles/inputFile.std] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Results validation:**

    -  Author : `François
       Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Luc
       Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
    -  Coded by : `François
       Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Luc
       Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to `WriterStd <WriterStd_8cpp.html>`__.

    Units tests

    | **Uses:**
    | **Used by:**

     
