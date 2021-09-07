\*\* Français

**Description:**

-  Calcul de la dépression du point de rosée, une mesure de l'humidité
   atmosphérique.
-  Écart entre la température d'une parcelle d'air et la température à
   laquelle l'air de cette parcelle doit être refroidie, à pression et
   contenu en humidité constants, pour atteindre la saturation.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air, TT

| \*et\* un des champs suivants :

-  Température du point de rosée, TD
-  Rapport de mélange de la vapeur d'eau, QV
-  Humidité spécifique, HU
-  Humidité relative, HR

\*Résultat(s):\*

-  Dépression du point de rosée, ES (deg C)

\*Algorithme:\*

.. code:: example

        -Si la clé --RPN n'est pas activée:

            *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
             le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
             l'humidité relative, HR (fraction) et la température de l'air, TT (deg C):

                Calculer la température du point de rosée, TD (deg C) avec le plugin TemperatureDewPoint.
                L'écart du point de rosée, ES (deg C ou deg K) est calculé selon :
                   ES = TT - TD  (si ES < 0.0 , ES = 0.0)
                où TT ou TD sont dans les mêmes unités (deg C ou deg K)

            *Si les champs d'entrée sont la température du point de rosée, TD (deg C ou deg K) et la température de l'air, TT (deg C ou deg K):

                L'écart du point de rosée, ES (deg C ou deg K) est calculé selon :
                   ES = TT - TD  (si ES < 0.0 , ES = 0.0)
                où TT ou TD sont dans les mêmes unités (deg C ou deg K)


        -Si la clé --RPN est activée:

            *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) et la température de l'air, TT (deg K):

                Calculer la pression, PX (Pa) avec le plugin Pressure.
                Appeler la fonction shuaes.ftn90 pour obtenir l'écart du point de rosée, ES (deg C ou deg K).

            *Si les champs d'entrée sont le rapport de mélange de la vapeur d'eau, QV (kg/kg) et la température de l'air, TT (deg K):

                Calculer l'humidité spécifique, HU (kg/kg) avec le plugin HumiditySpecific.
                Calculer la pression, PX (Pa) avec le plugin Pressure.
                Appeler la fonction shuaes.ftn90 pour obtenir l'écart du point de rosée, ES (deg C ou deg K).

            *Si les champs d'entrée sont l'humidité relative, HR (fraction) et la température de l'air, TT (deg K):

                Calculer la pression, PX (Pa) avec le plugin Pressure.
                Appeler la fonction shraes.ftn90 pour obtenir l'écart du point de rosée, ES (deg C ou deg K).

            *Si les champs d'entrée sont la température du point de rosée, TD (deg C ou deg K) et la température de l'air, TT (deg C ou deg K):
                ES = TT - TD  (si ES < 0.0 , ES = 0.0)
                où l'écart du point de rosée, ES est en deg C ou deg K

    Notes:  Lorsque le champ d'entrée est TD ou HR, le changement de phase sera présumé survenir au même moment dans le champ
            d'entrée que dans le champ de sortie.
            Lorsque plusieurs champs des dépendances et le champ TT sont disponibles en entrée, le calcul sera effectué
            avec le champ qui a le plus de niveaux en commun avec TT dans l'ordre de préférence (en cas d'égalité)
            avec HU suivi de QV, HR et finalement TD.
            Lorsque la clé --RPN est activée et l'attribut de --iceWaterPhase est BOTH, --temperaturePhaseSwitch n'est
            pas accepté et 273.16K (le point triple de l'eau) est attribué aux fonctions shuaes.ftn90 et shraes.ftn90.
            Avec la clé --RPN activée, les fonctions shuaes.ftn90 et shraes.ftn90 comparent la température du point de
            rosée avec 273.16K (le point triple de l'eau) pour choisir si on calcule l'écart du point de rosée par
            rapport à l'eau ou la glace.
            Sans la clé --RPN, on compare la température avec --temperaturePhaseSwitch pour choisir si on calcule
            l'écart du point de rosée par rapport à l'eau ou la glace.

**Références:**

-  `Librairie thermodynamique de
   RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipédia : point de
   rosée <http://fr.wikipedia.org/wiki/Point_de_ros%C3%A9e>`__
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2][Alduchov,
   O. A., and R. E. Eskridge, 1996: Improved Magnus form approximation
   of saturation vapor pressure. ''J. Appl. Meteor.'', '''35''',
   601-609.]]

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint,
   humidité/humidity

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/DewPointDepression/testsFiles/inputFile.std] >>
                [DewPointDepression --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Daniel Figueras <file:///wiki/Daniel_Figueras>`__
-  Codé par : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à to

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

English
-------

**Description:**

-  Calculation of the dew point depression, a measure of atmospheric
   humidity
-  Difference between the temperature of an air parcel and the
   temperature at which the air of that parcel must be cooled, at
   constant pressure and humidity content, to attain saturation.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature, TT

| \*and\* one of the following fields:

-  Dew point temperature, TD
-  Water vapour mixing ratio, QV
-  Specific humidity, HU

\*Result(s):\*

-  Dew point depression, ES (deg C)

\*Algorithm:\*

.. code:: example

    -If the --RPN key is NOT activated:

        *If the input fields are the specific humidity, HU (kg/kg) or
            the water vapour mixing ratio, QV (kg/kg) or
            the relative humidity, HR (fraction) and the air temperature, TT (deg C):

            Calculate the dew point temperature, TD (deg C) with the TemperatureDewPoint plug-in
            The dew point depression, ES (deg C or deg K) is calculated according to :
            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where TT or TD have the same units (deg C or deg K)

        *If the input fields are the dew point temperature, TD (deg C or deg K) and the air temperature, TT (deg C or deg K):

            The dew point depression, ES (deg C or deg K) is calculated according to :
            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where TT or TD have the same units (deg C or deg K)


    -If the --RPN key is activated:

        *If the input fields are the specific humidity, HU (kg/kg) and the air temperature, TT (deg K):

            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shuaes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the water vapour mixing ratio, QV (kg/kg) and the air temperature, TT (deg K):

            Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in
            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shuaes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the relative humidity, HR (fraction) and the air temperature, TT (deg K):

            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shraes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the dew point temperature, TD (deg C or deg K) and the air temperature, TT (deg C or deg K):

            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where the dew point depression, ES is in deg C or deg K

    Notes:  When the input field is TD or HR, the phase change will presumably happen at the same time in the input field as in output field.
            When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by QV, HR and finally TD.
            When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the shuaes.ftn90 and shraes.ftn90 functions.
            With the --RPN key activated, the functions shuaes.ftn90 and shraes.ftn90 compare the dew point temperature with 273.16K (the triple point of water) to select if we calculate the dew point depression with respect to water or ice.
            Without the --RPN key, we compare the temperature with --temperaturePhaseSwitch to select if we calculate the dew point depression with respect to water or ice.

**Reference:**

-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipédia : dew point <http://en.wikipedia.org/wiki/Dew_point>`__
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2][Alduchov,
   O. A., and R. E. Eskridge, 1996: Improved Magnus form approximation
   of saturation vapor pressure. ''J. Appl. Meteor.'', '''35''',
   601-609.]]

\*Keywords:\*

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint,
   humidité/humidity

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/DewPointDepression/testsFiles/inputFile.std] >>
                [DewPointDepression --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Daniel Figueras <file:///wiki/Daniel_Figueras>`__
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 

 
