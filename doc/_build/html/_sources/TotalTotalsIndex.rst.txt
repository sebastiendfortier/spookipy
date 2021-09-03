Français
--------

**Description:**

-  Calcul de l'indice total-total, un indice de temps violent utilisé
   comme prédicteur d'orages (Miller, 1972).
-  Cet indice combiné est une mesure du gradient thermique vertical et
   de l'humidité à bas niveaux.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air (TT) à 850 mb et 500 mb
   **et** un des champs suivants à 850 mb:
-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Humidité relative, HR
-  Température du point de rosée, TD
-  Écart du point de rosée (ES)

\*Résultat(s):\*

-  Indice "Total-Total", TTI (scalaire, sans unité)

\*Algorithme:\*

.. code:: example

    Soit TT850 et TT500, la température de l'air (deg C) à 850 mb et 500 mb respectivement.
    Soit TD850, la température du point de rosée (deg C) à 850 mb

    *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
        le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
        l'humidité relative, HR (fraction) ou
        l'écart du point de rosée, ES (deg C ou deg K) et la température de l'air, TT (deg C):

        Calculer la température du point de rosée, TD (deg C) avec le plugin TemperatureDewPoint avec --iceWaterPhase WATER.

        L'indice total-total est calculé selon :
          TTI = TT850 + TD850 - 2*(TT500)

    *Si les champs d'entrée sont la température du point de rosée, TD (deg C) et la température de l'air, TT (deg C):

        L'indice total-total est calculé selon :
          TTI = TT850 + TD850 - 2*(TT500)

**Références:**

-  Djurik,D 1994:Weather Analysis, Prentice-Hall
-  `Wikipedia: indice
   total-total <http://fr.wikipedia.org/wiki/Indice_total-total>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, stabilité/stability, indice/index, total,
   violent/severe, orage/thunderstorm, convection

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TotalTotalsIndex/testsFiles/inputFile.std] >>
                [TotalTotalsIndex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `George
   Karaganis <https://wiki.cmc.ec.gc.ca/wiki/User:Karaganisg>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

English
-------

**Description:**

-  Calculation of the Total Totals index, a severe weather index used
   for forecasting thunderstorms (Miller, 1972).
-  This combined index is a measure of the vertical lapse rate and of
   the humidity at low levels.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature (TT) at 850 mb and 500 mb
   **and** one of the following fields at 850 mb:
-  Specific Humidity, HU
-  Water vapour mixing ratio, QV
-  Relative Humidity, HR
-  Dew point temperature, TD
-  Dew point depression, ES

\*Result(s):\*

-  Total Totals index, TTI (scalar, without units)

\*Algorithm:\*

.. code:: example

    For TT850 and TT500, the air temperature (deg C) at 850 mb and 500 mb respectively.
    For TD850, the dew point temperature (deg C) at 850 mb.

    *If the input fields are the specific humidity, HU (kg/kg) or
        the water vapour mixing ratio, QV (kg/kg) or
        the relative humidity, HR (fraction) or
        the dew point depression, ES (deg C or deg K) and the air temperature, TT (deg C):

        Calculate the dew point temperature, TD (deg C) with TemperatureDewPoint plug-in with --iceWaterPhase WATER.

        The Total Totals index is calculated as :
          TTI = TT850 + TD850 - 2*(TT500)

    *If the input fields are the dew point temperature, TD (deg C) and the air temperature, TT (deg C):

        The Total Totals index is calculated as :
          TTI = TT850 + TD850 - 2*(TT500)

**Reference:**

-  Djurik,D 1994:Weather Analysis, Prentice-Hall.
-  `Wikipedia : Total Totals index (link only in
   French) <http://fr.wikipedia.org/wiki/Indice_total-total>`__

\*Customizable condition:\*

-  Height for bottom and top levels in mb

\*Keywords:\*

-  MÉTÉO/WEATHER, stabilité/stability, indice/index, total,
   violent/severe, orage/thunderstorm, convection

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TotalTotalsIndex/testsFiles/inputFile.std] >>
                [TotalTotalsIndex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `George
   Karaganis <https://wiki.cmc.ec.gc.ca/wiki/User:Karaganisg>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 

 
