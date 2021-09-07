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

 
