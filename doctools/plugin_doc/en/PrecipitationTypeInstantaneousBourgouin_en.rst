English
-------

**Description:**

-  Calculation of the type of instantaneous precipitation by using the
   Bourgouin method, based on the available energy in the cold and warm
   layers in altitude. More specifically, this method examines the
   temperature profile and takes into account the positive and negative
   energies with respect to the 0 deg C isotherm to decide the type of
   precipitation according to the energetic reference values. The
   positive energy (negative) is defined here as the area on a tephigram
   where the temperature is positive (negative, respectively).
-  The energy layers, obtained by the mean isotherm method ( plug-in),
   are delimited by the freezing levels (in pressure) produced by the
   plug-in.

\*Iteration method:\*

-  Column-by-column

\*Dependencies:\*

-  Air temperature, TT
-  Total precipitation rate, RT
   ***Note:*** Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results called by this plug-in (see
   the section "this plug-in uses"). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

\*Result(s):\*

-  Type of instantaneous precipitation, T6 (2D, no units). Coded value
   from 1 to 6 such as :
   1: rain
   2: mixed rain/snow
   3: freezing rain
   4: ice pellets
   5: snow
   6: insufficient precipitation rate (less than 0.2mm/h)

\*Algorithm:\*

-  https://wiki.cmc.ec.gc.ca/images/f/f2/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.doc
-  https://wiki.cmc.ec.gc.ca/images/4/4b/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.pdf

\*Reference:\*

-  Reference article on the Bourgouin method :
   https://wiki.cmc.ec.gc.ca/images/5/59/Spooki_-_Article_ref_Bourgouin.pdf
-  Inspired from the operational program ''gembrgouin''

\*Keywords:\*

-  MÉTÉO/WEATHER, énergie/energy, aire/area, isotherme/isotherm,
   méthode/method , téphigramme/tephigram

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationTypeInstantaneousBourgouin/testsFiles/inputFile.std] >>
                ( [Copy] + [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 10 ]  ) >>
                [PrecipitationTypeInstantaneousBourgouin] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
