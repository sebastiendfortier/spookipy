Français
--------

**Description:**

-  Calcul de l'indice SWEAT (Severe Weather Threat Index), un indice de
   temps violent utilisé pour déterminer la probabilité d'orages
   violents et de tornades (Miller, 1972).
-  Cet indice de convection consiste en un terme d'instabilité (indice
   total-total), un terme d'humidité à bas niveaux et des termes
   d'écoulement, dont un terme de cisaillement.
-  La combinaison de ces trois termes permet de discriminer les orages
   violents des orages ordinaires, dont le potentiel peut être évalué
   par l'indice total-total ou l'indice de soulèvement.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air (TT) à 850 mb et 500 mb
-  Composante UU du vent (selon l'axe des X) à 850 mb et 500 mb
-  Composante VV du vent (selon l'axe des Y) à 850 mb et 500 mb
   **et** un des champs suivants à 850 mb:
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

-  Indice SWEAT, SW (scalaire, sans unité)

\*Algorithme:\*

.. code:: example

    Soit TTI, l'indice total-total
    Soit TD850, la température du point de rosée (deg C) à 850 mb
    Soit UV850 et UV500, le module du vent (noeuds) à 850 mb et 500 mb respectivement
    Soit WD850 et WD500, la direction du vent (deg) à 850 mb et 500 mb respectivement

    *Si les champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou
        le rapport de mélange de la vapeur d'eau, QV (kg/kg) ou
        l'humidité relative, HR (fraction) ou
        l'écart du point de rosée, ES (deg C ou deg K) et la température de l'air, TT (deg C) et
        les composantes du vent, UU et VV:

        Calculer la température du point de rosée, TD (deg C) avec le plugin TemperatureDewPoint avec --iceWaterPhase WATER.

        L'indice SWEAT (SW) est calculé selon l'équation (Miller, 1972) :
           SW = 12*TD850 + 20*(TTI-49) + 2*UV850 + UV500 + 125*(S + 0.2)
        où S = sin(WD500 - WD850)

    *Si les champs d'entrée sont la température du point de rosée, TD (deg C) et la température de l'air, TT (deg C):

        L'indice SWEAT (SW) est calculé selon l'équation (Miller, 1972) :
           SW = 12*TD850 + 20*(TTI-49) + 2*UV850 + UV500 + 125*(S + 0.2)
        avec :  S = sin(WD500 - WD850)

    - Le terme [12*TD850] = 0 si TD850 < 0
    - Le terme d'instabilité  [20*(TTI-49)] = 0  si TTI < 49
    - Le terme de cisaillement  [125*(S + 0.2)] = 0  si l'une des conditions suivantes n'est pas
      remplie :
      - 130 deg <=  WD850  <= 250 deg
      - 210 deg <=  WD500  <= 310 deg
      - WD500 - WD850 > 0
      - UV850 >= 15 noeuds et UV500 >= 15 noeuds

    ATTENTION: L'indice SWEAT est très sensible à TD850. Des différences significatives peuvent être obtenues dans la valeur du SWEAT selon
               la variable d'humidité utilisée pour calculer TD850. Voir l'algorithme du plugin TemperatureDewPoint quant à la prévalence de
               la variable d'humidité utilisée pour calculer la température du point de rosée.

**Références:**

-  [[https://wiki.cmc.ec.gc.ca/images/d/dd/Spooki_-_Severe_Weather_Forecasting.pdf][Severe
   Weather Forecasting:Post-Processing NWP outputs and guidance at the
   CMC; R. Verret, G. Desautels, A. Bergeron]]
-  Djurik,D 1994:Weather Analysis, Prentice-Hall.
-  `Wikipedia: indice
   SWEAT <http://fr.wikipedia.org/wiki/Indice_de_menace_de_temps_violent>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, stabilité/stability, convection, indice/index,
   violent/severe, orage/thunderstorm, tornade/tornado

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SweatIndex/testsFiles/inputFile.std] >>
                [SweatIndex] >>
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

 
