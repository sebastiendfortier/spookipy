English
-------

**Description:**

-  Limit the minimum of a field to the specified value

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field of which no value is less than the specified
   value

\*Algorithm:\*

.. code:: example

    For F, a given field of size N, composed of n elements (n = 1,N)

    For z, a value given by the "value" key, designated as the lower boundary of the field F

    For each point n=1,N do

        If F(n) < z then
           F(n) = z
        End if

    End do

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, minimum, borne/bound, inférieur/lower

\*Usage:\* htmlonly<iframe id="usage"
src="forward2python.php/spooki\ :sub:`createdynamicdocparts`/usage/SetLowerBoundary"
width="100%" frameborder="0" scrolling="no"
onload="resizeFrame(document.getElementById('usage'))"></iframe>

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetLowerBoundary/testsFiles/inputFile.std] >>
                [SetLowerBoundary --value 1 ] >>
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

 
