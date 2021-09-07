English
-------

**Description:**

-  Find the atmospheric pressure for the surface of a constant field.

\*Iteration method:\*

-  Column by column

\*Dependencies:\*

-  A 3D field

\*Result(s):\*

-  Pressure of the surface of a constant field, PXXX (hPa)

\*Algorithm:\*

.. code:: example

    For PDS ,          a 3D field.
    For PX (hPa),      the pressure of the model.
    For PXXX (hPa),    the pressure of the surface of a constant field.
    For FIELDCONSTANT, the desired values.

    Initialize to -1 all points in PXXX matrix
    Loop from the top or the bottom depending on --scanDirection value.
    If necessary, invert the matrix before the search (depending on --scanDirection).

    Loop on the columns of the matrix (i * j):
       Loop on the FIELDCONSTANT values (p): 
            Loop on the column levels (k), skipping the first and last levels:    
                If a crossover is found between the field PDS and FIELDCONSTANT (between levels k and k-1):
                    Calculate PXXX (see formula below) 
                End if
            End of loop on column levels (k)
        End of loop on FIELDCONSTANT values (p)
    End of loop on columns

    PXXX calculation:
       If (abs( PDS(k) - PDS(k - 1) ) <= 1E-5)
          :math:`\mathrm{ PXXX_{p} = PX_{k} }`
       Else
          :math:`\mathrm{ AAA = 1 / ( PDS_{k} - PDS_{k - 1} ) }`
         
    :math:`\mathrm{ WEIGHT = AAA * ( FIELDCONSTANT_{p} - PDS_{k - 1} )
    }`
         
    :math:`\mathrm{ WEIGHTMINUS = AAA * ( PDS_{k} - FIELDCONSTANT_{p} )
    }`
         
    :math:`\mathrm{ PXXX_{p} = PX_{k} * WEIGHT + PX_{k - 1} * WEIGHTMINUS
    }`
       End if

**Reference:**

-  Does not apply

\*Keywords:\*

-  MÉTÉO/WEATHER, isoplèthe/isopleth, pression/pressure

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PressureOnIsopleth/testsFiles/inputFile.std] >>
                [PressureOnIsopleth --fieldName TT --scanDirection DESCENDING --fieldConstant 20.0,25.0,30.0 --outputFieldName PXXX] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Coded by : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
