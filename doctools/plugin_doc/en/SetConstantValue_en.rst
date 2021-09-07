English
-------

**Description:**

-  the input field and replace all its values by a given constant.
   Possibility to generate a 2D constant field from a 3D field.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  A copy (3D or 2D) of the meteorological field received from input
   containing the value received as parameter

\*Algorithm:\*

-  Does not apply

\*Reference:\*

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, constant, generate/produire

\*Usage:\*

    \*/\ `Notes:/\*\\\\ <Notes:/*\\>`__ For the '--value' option:

    -  MAXINDEX: the index number of the last level of the input field
    -  MININDEX: the index number of the first level of the input field
    -  NBLEVELS: the number of levels of the input field

    \*Call example:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std] >>
                    [SetConstantValue --value 4.0] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Results validation:**

    **Contacts:**

    -  Author : `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
    -  Coded by : `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to

    Units tests

    | **Uses:**
    | **Used by:**

     
