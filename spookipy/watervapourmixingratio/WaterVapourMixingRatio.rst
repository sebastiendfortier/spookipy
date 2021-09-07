Français
--------

**Description:**

-  Calcul du rapport de mélange de la vapeur d'eau, rapport entre la
   masse de vapeur d'eau et la masse d'air sec.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Humidité spécifique, HU
   ou
-  Température de l'air, TT
   **et** un des champs suivants:
-  Humidité relative, HR
-  Température du point de rosée, TD / Écart du point de rosée, ES

\*Résultat(s):\*

-  Rapport de mélange de la vapeur d'eau, QV (g kg-1)

\*Algorithme:\*

.. code:: example

        -Si la clé --RPN n'est pas activée:

            *Si le champ d'entrée est l'humidité spécifique, HU (kg/kg):
                QV = HU / (1-HU)
                où QV est le rapport de mélange de la vapeur d'eau en kg/kg.

            *Si les champs d'entrée sont l'humidité relative HR (fraction) ou
                la température de point de rosée, TD (deg C)/ écart du point de rosée, ES (deg K ou deg C) et
                la température de l'air, TT (deg C):

                Calculer la pression de vapeur, VPPR (Pa) avec le plugin VapourPressure.
                Calculer la pression, PX (Pa) avec le plugin Pressure.
                QV = epsilon * [VPPR/(PX-VPPR)]
                où QV est le rapport de mélange de la vapeur d'eau en kg/kg et
                epsilon est défini dans la table des constantes comme 0.6219800221014e+00 et correspond à Rd/Rv .


        -Si la clé --RPN est activée:

            *Si le champ d'entrée est l'humidité spécifique, HU (kg/kg):
                QV = HU / (1-HU)
                où QV est le rapport de mélange de la vapeur d'eau en kg/kg.

            *Si les champs d'entrée sont l'humidité relative HR (fraction) ou
                la température de point de rosée, TD (deg C)/ écart du point de rosée, ES (deg K ou deg C) et
                la température de l'air, TT (deg C):

                Calculer l'humidité spécifique, HU (kg/kg) avec le plugin HumiditySpecific (avec les mêmes clés et leurs arguments).
                QV = HU / (1-HU)
                où QV est le rapport de mélange de la vapeur d'eau en kg/kg.


        Convertir QV en g/kg:
           QV(g/kg) = QV(kg/kg)*1000.0


    Notes:  Lorsque plusieurs champs des dépendances et le champ TT sont disponibles en entrée, le calcul sera effectué avec le champ qui a le plus de niveaux en commun avec TT dans l'ordre de préférence (en cas d'égalité) avec HU suivi de HR et finalement ES/TD.
            Lorsque le champ TT n'est pas disponible, le calcul sera effectué avec HU.
            Lorsque la clé --RPN est activée et l'attribut de --iceWaterPhase est BOTH, --temperaturePhaseSwitch n'est
            pas accepté et 273.16K (le point triple de l'eau) est attribué aux onctions sesahu.ftn90 et shrahu.ftn90
            qui sont appelées par le plugin HumiditySpecific.

**Références:**

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.
-  `Analyse du rapport de mélange de la vapeur
   d'eau <https://wiki.cmc.ec.gc.ca/wiki/RPT/Analyse_du_rapport_de_m%C3%A9lange_de_la_vapeur_d%27eau>`__
-  `Librairie thermodynamique
   RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf%20>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, humidité/humidity, rapport/ratio, pression/pressure

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WaterVapourMixingRatio/testsFiles/inputFile.std] >>
                [WaterVapourMixingRatio] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : Neil Taylor
-  Codé par : Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| Voir la référence à
| Tests unitaires
| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

English
-------

**Description:**

-  Calculates the water vapour mixing ratio, which is the ratio of the
   mass of water vapour to the mass of dry air.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Specific humidity, HU or
-  Air temperature, TT and one of the following fields:
-  Relative humidity, HR
-  Dewpoint temperature, TD / Dewpoint depression, ES

NOTE: Make sure to provide the dependencies listed above to this plug-in
or to the plug-in results called by this plug-in (see the section "this
plug-in uses"). For more details on this alternative use, see the
`documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
page.

**Result(s):**

-  Water vapour mixing ratio, QV (g kg-1)

\*Algorithm:\*

.. code:: example

        -If the --RPN key is NOT activated:

            *If the input field is specific humidity, HU (kg/kg):
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.


            *If the input fields are relative humidity, HR (fraction) or
                dew point temperature, TD (deg C)/ dew point depression, ES (deg K or deg C) and
                the air temperature, TT (deg C):

                Calculate the vapour pressure, VPPR (Pa) with the VapourPressure plug-in.
                Calculate the pressure, PX (Pa) with the Pressure plug-in.
                QV = epsilon * [VPPR/(PX-VPPR)]
                where QV is the water vapour mixing ratio in kg/kg and
                epsilon is defined in the table of constants as 0.6219800221014e+00 and corresponds to Rd/Rv.


        -If the --RPN key is activated:

            *If the input field is specific humidity, HU (kg/kg):
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.

            *If the input fields are relative humidity, HR (fraction) or
                dew point temperature, TD (deg C)/ dew point depression, ES (deg K or deg C) and
                the air temperature, TT (deg C):

                Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in (with the same keys as their arguments)
                QV = HU / (1-HU)
                where QV is the water vapour mixing ratio in kg/kg.


        Convert QV in g/kg:
            QV(g/kg) = QV(kg/kg)*1000.0


    Notes: When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by HR and finally ES/TD.
           When the TT field is not available, the calculation will be done in order of preference with HU.
           When the --RPN key is activate and the attribute to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the sesahu.ftn90 and shrahu.ftn90 functions which are called by the HumiditySpecific plug-in.

**Reference:**

-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.
-  `Analysis of water vapour mixing
   ratio <https://wiki.cmc.ec.gc.ca/wiki/RPT/en/Analysis_of_water_vapour_mixing_ratio>`__
-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf%20>`__

\*Keywords:\*

-  WEATHER/METEO, humidity/humidite, ratio/rapport, pressure/pression

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WaterVapourMixingRatio/testsFiles/inputFile.std] >>
                [WaterVapourMixingRatio] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| Reference to
| Units tests
| **Uses:**
| **Used by:**

 