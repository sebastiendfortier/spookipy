Français
--------

**Description:**

-  Calcul de l'humidité spécifique, rapport entre la masse de vapeur
   d'eau dans l'air et la masse d'air humide.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Rapport de mélange de la vapeur d'eau, QV
   ou
-  Température de l'air, TT
   **et** un des champs suivants:
-  Température du point de rosée, TD / Écart du point de rosée, ES
-  Humidité relative, HR

\*Résultat(s):\*

-  Humidité spécifique, HU (kg/kg)

\*Algorithme:\*

.. code:: example

        -Si la clé --RPN n'est pas activée:

            *Si le champ d'entrée est le rapport de mélange de la vapeur d'eau, QV (kg/kg):
                HU = QV / (QV+1)
                où l'humidité spécifique, HU est en kg/kg.

            *Si les champs d'entrée sont l'humidité relative, HR (fraction) ou
                la température du point de rosée, TD (deg C) / l'écart du point de rosée, ES (deg K ou deg C) et
                la température de l'air, TT (deg C):
                Calcul de la pression de vapeur, VPPR (Pa) avec le plugin VapourPressure.
                Calcul la pression, PX (Pa) avec le plugin Pressure.

                HU = epsilon * ( VPPR / (PX - (1-epsilon)*VPPR))

                où l'humidité spécifique, HU est en kg/kg et epsilon est défini dans la table des constantes
                comme 0.6219800221014e+00 et correspond à Rd/Rv.

        -Si la clé --RPN est activée:

            *Si le champ d'entrée est le rapport de mélange de la vapeur d'eau, QV (kg/kg):
                Il n'existe pas de fonction RPN pour ce calcul, nous utilisons donc:
                HU = QV / (QV+1)
                où l'humidité spécifique, HU est en kg/kg.

            *Si les champs d'entrée sont l'humidité relative, HR (fraction) et la température de l'air, TT (deg K):
                Calcul de la pression, PX (Pa) avec le plugin Pressure.
                Appeler la fonction shrahu.ftn90 pour obtenir l'humidité spécifique, HU (kg/kg).

            *Si les champs d'entrée sont la température du point de rosée, TD (deg K) / l'écart du point de rosée, ES (deg K ou deg C) et la température de l'air, TT (deg K):
                Calcul de l'écart du point de rosée, ES (deg K ou deg C) avec le plugin DewPointDepression si nécessaire.
                Calcul de la pression PX (Pa) avec le plugin Pressure.
                Appeler la fonction sesahu.ftn90 pour obtenir l'humidité spécifique, HU (kg/kg).


    Notes:  Lorsque plusieurs champs des dépendances et le champ TT sont disponibles en entrée, le calcul sera effectué
            avec le champ qui a le plus de niveaux en commun avec TT dans l'ordre de préférence (en cas d'égalité) avec
            QV suivi de HR, et finalement ES/TD.
            Lorsque le champ TT n'est pas disponible, le calcul sera effectué avec QV.
            Lorsque la clé --RPN est activée et l'attribut de --iceWaterPhase est BOTH, --temperaturePhaseSwitch n'est
            pas accepté et 273.16K (le point triple de l'eau) est attribué aux fonctions sesahu.ftn90 et shrahu.ftn90.

**Références:**

-  `Librairie thermodynamique de
   RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipedia : Humidité
   spécifique <http://fr.wikipedia.org/wiki/Humidit%C3%A9_sp%C3%A9cifique>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumiditySpecific/testsFiles/inputFile.std] >>
                [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Daniel Figueras <file:///wiki/Daniel_Figueras>`__
-  Codé par : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__, `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Units tests

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
English
-------

**Description:**

-  Calculation of the specific humidity, the ratio of the mass of water
   vapour in the air to the total mass of moist air.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Water vapour mixing ratio, QV
   or
-  Air temperature, TT
   **and** one of the following fields:
-  Dew point temperature, TD / Dew point depression, ES
-  Humidité relative, HR

\*Result(s):\*

-  Specific humidity, HU (kg/kg)

\*Algorithm:\*

.. code:: example

            -If the --RPN key is NOT activated:

              *If the input field is the water vapour mixing ratio, QV (kg/kg)
                   HU = QV / (QV + 1)
                 where the specific humidity, HU is in kg/kg


              *If the input fields are the relative humidity, HR (fraction) or the dew point temperature, TD (deg C) / dew point depression, ES (deg K or deg C) and the air temperature, TT (deg C)
                 Calculation of the vapour pressure, VPPR (Pa) with the VapourPressure plug-in
                 Calculation of the pressure, PX (Pa) with the Pressure plug-in
                    HU = epsilon * ( VPPR / (PX - (1-epsilon)*VPPR))
                 where specific humidity, HU is in kg/kg and epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


            -If the --RPN key is activated:

              *If the input field is the water vapour mixing ratio, QV (kg/kg)
                 There is no RPN function for this calculation, therefore we use:
                   HU = QV / (QV + 1)
                 where the specific humidity, HU is in kg/kg

              *If the input fields are the relative humidity, HR (fraction) and the air temperature, TT (deg K)
                 Calculate the pressure, PX (Pa) with the Pressure plug-in
                 Call the function shrahu.ftn90 to obtain the specific humidity, HU (kg/kg)

              *If the input fields are the dew point temperature, TD (deg K) / the dew point depression, ES (deg K or deg C) and the air temperature, TT (deg K)
                 Calculate the dew point depression, ES (deg K or deg C) with the DewPointDepression plug-in if necessary
                 Calculate the pressure, PX (Pa) with the Pressure plug-in
                 Call the function sesahu.ftn90 to obtain the specific humidity, HU (kg/kg)


    Notes:  - When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with QV followed by HR and finally ES/TD.
            - When the TT field is not available, the calculation will be done with QV.
            - When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the sesahu.ftn90 and shrahu.ftn90 functions.

**Reference:**

-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipedia : Specific
   humidity <http://en.wikipedia.org/wiki/Specific_humidity>`__

\*Keywords:\*

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumiditySpecific/testsFiles/inputFile.std] >>
                [HumiditySpecific --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Daniel Figueras <file:///wiki/Daniel_Figueras>`__
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__, `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
