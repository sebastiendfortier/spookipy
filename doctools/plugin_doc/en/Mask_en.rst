English
-------

**Description:**

-  This plug-in creates a mask according to the threshold value(s)
   given.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A field

\*Result(s):\*

-  MASK field

\*Algorithm:\*

.. code:: example

    For F,             an input field
    For thresholds[j], jth value given in the list of --thresholds option
    For operator[j],   jth value given in the list of --operators option
    For value[j],      jth value given in the list of --values option
    For nbTrios,       the total number of threshold, operator and value trios

    For each point of the input field (i)

      Initialize MASK = 0.0

      For j = 0 to (nbTrios - 1)

        If F[i]  Operators[j]  Thresholds[j]
           MASK[i]=Value[j]
        Endif

      End for

    End for

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, masque/mask

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Mask/testsFiles/inputFile.std] >> 
                [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators GE,GE,GE,GE] >> 
                [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion]"
    ...

**Results validation:**

**Contacts:**

-  Auteur(e) : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__, / `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__
-  Codé par : `Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Faustl>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to .

Units tests

| **Uses:**
| **Used by:**

 
