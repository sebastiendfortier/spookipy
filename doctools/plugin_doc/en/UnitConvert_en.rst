English
-------

**Description:**

-  Converts all the data received into a compatible unit
-  The list of all the valid units is available `here <units.html>`__
-  Possibility of converting the data received into default units in the
   `database <stdvar.html>`__

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Fields with valid units

\*Result(s):\*

-  Input fields converted into a given compatible unit

\*Algorithm:\*

-  Apply the conversion factor to each data point
-  If the "STD" unit is chosen,

   -  all the data is converted with the help of compatible units
      described in the database
   -  if the field does not exist in the database, the plug-in stops and
      warns the user, unless the "ignoreMissing" key is activated, in
      this case, no conversion is made

\*Reference:\*

-  `Units database <units.html>`__
-  `Variables database <stdvar.html>`__

\*Keywords:\*

-  SYSTÈME/SYSTEM, unité/unit, convertir/convert

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/UnitConvert/testsFiles/inputFile.std] >>
                [UnitConvert --unit kilometer_per_hour] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Tests unitaires

| **Uses:**
| **Used by:**

 
