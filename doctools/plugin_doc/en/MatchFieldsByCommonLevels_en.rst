English
-------

**Description:**

-  Find, amongst the fields specified, the field with the greater number
   of common levels with the given reference field.

\*Iteration method:\*

-  Does not apply

\*Dependencies:\*

-  At least two fields as input

\*Result(s):\*

-  The field with the greater number of common levels with the reference
   field.
-  The reference field.

\*Algorithm:\*

.. code:: example

    - Find, amongst the fields given with the parameterizable key --matchFields, the field with the greater number of common vertical levels with the reference field.

    - Return that field and the reference field on those common levels.

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, sélection/selection, correspondance/match,
   niveaux/levels

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MatchFieldsByCommonLevels/testsFiles/inputFile.std] >>
                [MatchFieldsByCommonLevels --referenceField TT --matchFields HU,HR,ES,TD] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  

\*Contacts:\*

-  Author : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
