Français
--------

**Description:**

-  Calcul de l'indice de George-K , un indice de temps violent utilisé
   comme prédicteur d'orages (George, 1960).
-  Cet indice tient compte du gradient vertical de température et de
   l'humidité dans les bas niveaux.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air (TT) à 850 mb, 700 mb et 500 mb
   **et** un des champs suivants à 850 mb et 700 mb:
-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Humidité relative, HR
-  Température du point de rosée, TD
-  Écart du point de rosée, ES
   ***Note:*** : Assurez-vous de fournir à ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s):\*

-  Indice de George-K, KI (scalaire sans unité)

\*Algorithme:\*

.. code:: example

    Soit TT850, TT700 et TT500, la température de l'air (deg C) à 850mb, 700mb et 500mb respectivement.
    Soit TD850 et TD700, la température du point de rosée (deg C) à 850mb et 700mb respectivement.

    *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
        le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
        l'humidité relative, HR (fraction) ou
        l'écart du point de rosée, ES (deg C ou deg K) et la température de l'air, TT (deg C):

        Calculer la température du point de rosée, TD (deg C) avec le plugin TemperatureDewPoint avec --iceWaterPhase WATER.

        KI = (TT850 - TT500) + TD850 - (TT700 - TD700)
        où KI est l'indice de George-K (scalaire)

    *Si les champs d'entrée sont la température du point de rosée, TD (deg C) et la température de l'air, TT (deg C):

        KI = (TT850 - TT500) + TD850 - (TT700 - TD700)
        où KI est l'indice de George-K (scalaire)

**Références:**

-  George, J.J., 1960; Weather Forecasting for Aeronautics, Academic
   Press
-  Bluestein, 1993; Synoptic-Dynamic Meteorology in Midlatitudes, Oxford
   University Press, Vol 2, 594pp.
-  `Wikipedia: indice de
   George <http://fr.wikipedia.org/wiki/Indice_de_George>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, indice/index, George, violent/severe,
   orage/thunderstorm, convection, stabilité/stability

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/GeorgeKIndex/testsFiles/inputFile.std] >>
                [GeorgeKIndex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : George Karaganis
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
