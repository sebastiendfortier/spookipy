English
-------

**Description :**

-  Calculates the virtual temperature as a function of temperature and
   water vapour mixing ratio.
-  The virtual temperature is used to account for the presence of water
   vapour and may be interpreted as a proxy for density.

\*Méthode d'itération :\*

-  Point-by-point

\*Dépendances :\*

-  Relative humidity (HR)
-  Air Temperature (TT)
-  Atmospheric pressure (PX) ***Note:*** : Make sure to provide the
   dependencies listed above to this plug-in or to the plug-in results
   called by this plug-in (see the section "this plug-in uses"). For
   more details on this alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

\*Résultat(s) :\*

-  Virtual temperature, VT (deg C)

\*Algorithme :\*

.. code:: example

    For QV the water vapour mixing ratio (kg/kg)
    For TT the air temperature in deg K
    The virtual temperature (deg K) is calculated as:

.. code:: example

    VT(deg K) = TT*[(1+QV/epsilon)/(1+QV)]
    VT(deg C) = VT(deg K) - 273.15

.. code:: example

    Where epsilon is the ratio of Rd (the gas constant for dry air; Rd = 287.05 J/(kg*K)) and
    Rv (the gas constant for water vapour; Rv = 461.51 J/(kg*K)).

.. code:: example

**Références :**

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.
-  `Analysis of virtual
   temperature <https://wiki.cmc.ec.gc.ca/wiki/RPT/en/Analysis_of_virtual_temperature>`__

\*Mots clés :\*

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureVirtual/testsFiles/inputFile.std] >>
                [TemperatureVirtual] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit Tests

| **Uses:**
| **Used by:**

 
