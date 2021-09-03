Français
--------

**Description:**

-  Calcul de la température thermodynamique du point de rosée, une
   mesure de l'humidité atmosphérique.
-  Température à laquelle l'air doit être refroidi, à pression et
   contenu en humidité constants, pour atteindre la saturation.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air, TT
   **et** un des champs suivants:
-  Écart du point de rosée, ES
-  Humidité spécifique, HU
-  Humidité relative, HR
-  Rapport de mélange de la vapeur d'eau, QV

\*Résultat(s):\*

-  Température du point de rosée, TD (deg C)

\*Algorithme:\*

.. code:: example

        -Si la clé --RPN n'est pas activée:

            *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
             le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
             l'humidité relative, HR (fraction) et la température de l'air, TT (deg C):

                 Soit TPL, la température à laquelle il faut changer de la saturation par rapport à l'eau à la saturation par rapport à la glace (deg C).
                 Calculer la pression de vapeur, VPPR (hPa) avec le plugin VapourPressure.
                 Calculer la température du point de rosée, TD (deg C):

                 Si TT > TPL ou --iceWaterPhase WATER
                   TD= ( AEw3 * ln(VPPR/AEw1) ) / ( AEw2 - ln (VPPR/AEw1) )
                 Sinon
                   TD= ( AEi3 * ln(VPPR/AEi1) ) / ( AEi2 - ln (VPPR/AEi1)

                 où selon Alduchov et Eskridge (1996)
                  AEw1=6.1094   AEi1=6.1121
                  AEw2=17.625   AEi2=22.587
                  AEw3=243.04   AEi3=273.86

            *Si les champs d'entrée sont l'écart du point de rosée, ES (deg C ou deg K) et la température de l'air, TT (deg C):

                TD = TT - ES   (si ES < 0.0 , ES = 0.0)
                où TD est la température du point de rosée (deg C)

        -Si la clé --RPN est activée:

            *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
             le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
             l'humidité relative, HR (fraction), et la température de l'air TT (deg C):

                Calculer l'écart du point de rosée, ES (deg C ou deg K) avec le plugin DewPointDepression (avec les mêmes clés et leurs arguments).

                TD = TT - ES   (si ES < 0.0 , ES = 0.0)
                où TD est la température du point de rosée (deg C)

            *Si les champs d'entrées sont TT (deg C) et ES (deg C ou deg K):

                TD = TT - ES  (si ES < 0.0 , ES = 0.0)
                où TD est la température du point de rosée (deg C)

    Notes: Lorsque le champ d'entrée est ES ou HR, le changement de phase sera présumé survenir au même moment dans
           le champ d'entrée que dans le champ de sortie.
           Lorsque plusieurs champs des dépendances et le champ TT sont disponibles en entrée, le calcul sera effectué
           avec le champ qui a le plus de niveaux en commun avec TT dans l'ordre de préférence (en cas d'égalité)
           avec HU suivi de QV, HR et finalement ES.
           Lorsque la clé --RPN est activée et l'attribut de --iceWaterPhase est BOTH, --temperaturePhaseSwitch n'est
           pas accepté et 273.16K (le point triple de l'eau) est attribué aux fonctions shuaes.ftn90 et shraes.ftn90
           qui sont appelées par le plugin DewPointDepression.

**Références:**

-  `Wikipédia : point de
   rosée <http://fr.wikipedia.org/wiki/Point_de_rosée>`__
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2][Alducho
   v, O. A., and R. E. Eskridge, 1996: Improved Magnus form
   approximation of saturation vapor pressure. *J. Appl. Meteor.*,
   **35**, 601-609.]]
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/BAMS-86-2-225][Lawrence,
   M. G., 2005: The relationship between relative humidity and the
   dewpoint temperature in moist air: A simple conversion and
   applications. *Bull. Amer. Meteor.* Soc., **86**, 225-233.]]
-  `Librairie thermodynamique de
   RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint,
   humidité/humidity

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureDewPoint/testsFiles/inputFile.std] >>
                [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__, Jonathan
   Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
English
-------

**Description:**

-  Calculates the thermodynamic temperature of the dew point, a mesure
   of the atmospheric humidity.
-  Temperature at which the air must be cooled, at constant pressure and
   humidity content, to become saturated.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature, TT
   **and** one of the following fields:
-  Dew point depression, ES
-  Specific humidity, HU
-  Relative humidity, HR
-  Water vapour mixing ratio, QV

\*Result(s):\*

-  Dew point temperature, TD (deg C)

\*Algorithm:\*

.. code:: example

    -If the --RPN key is NOT activated:

        *If the input fields are the specific humidity, HU (kg/kg) or
         the water vapour mixing ratio, QV (kg/kg) or
         the relative humidity, HR (fraction) and the air temperature, TT (deg C):

            For TPL, the temperature at which we must change from the saturation with respect to water to the saturation with respect to ice (deg C)
            Calculate the vapour pressure, VPPR (hPa) with the VapourPressure plug-in
            Calculate the dew point temperature, TD (deg C):

            If TT > TPL or --iceWaterPhase WATER
               TD= ( AEw3 * ln(VPPR/AEw1) ) / ( AEw2 - ln (VPPR/AEw1) )
            else
               TD= ( AEi3 * ln(VPPR/AEi1) ) / ( AEi2 - ln (VPPR/AEi1) )

            where according to Alduchov and Eskridge (1996)
               AEw1=6.1094   AEi1=6.1121
               AEw2=17.625   AEi2=22.587
               AEw3=243.04   AEi3=273.86

        *If the input fields are the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C):

            TD = TT - ES   (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)


    -If the --RPN key is activated:

        *If the input fields are the specific humidity, HU (kg/kg) or
         the water vapour mixing ratio, QV (kg/kg) or
         the relative humidity, HR (fraction) and the air temperature TT (deg C):

            Calculate the dew point depression, ES (deg C or deg K) with the DewPointDepression plug-in (with the same keys and their arguments)

            TD = TT - ES  (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)

        *If the input fields are TT (deg C) and ES (deg C or deg K):

            TD = TT - ES  (if ES < 0.0 , ES = 0.0)
            where TD is the dew point temperature (deg C)


    Notes:  - When the input field is ES or HR, the phase change will presumably happen at the same time in the input field as in output field.
            - When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality)
              with HU followed by QV, HR and finally ES.
            - When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, -temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the shuaes.ftn90 and shraes.ftn90 functions which are called by the DewPointDepression plug-in.

**Reference:**

-  (FRENCH) `Wikipédia : point de
   rosée <http://fr.wikipedia.org/wiki/Point_de_rosée>`__
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2][Alducho
   v, O. A., and R. E. Eskridge, 1996: Improved Magnus form
   approximation of saturation vapor pressure. *J. Appl. Meteor.*,
   **35**, 601-609.]]
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/BAMS-86-2-225][Lawrence,
   M. G., 2005: The relationship between relative humidity and the
   dewpoint temperature in moist air: A simple conversion and
   applications. *Bull. Amer. Meteor.* Soc., **86**, 225-233.]]
-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

\*Keywords:\*

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint,
   humidité/humidity

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureDewPoint/testsFiles/inputFile.std] >>
                [TemperatureDewPoint --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__, Jonathan
   Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
