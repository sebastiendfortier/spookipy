Français
--------

**Description:**

-  Calcul de l'humidex. L'humidex est un indice qui vise à quantifier
   l'inconfort créé par une combinaison de la chaleur et de l'humidité.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  | Température de l'air en surface (TTC) .
   | **et** un des champs suivants à la surface:

-  Humidité spécifique, HU

-  Humidité relative, HR

-  Rapport du mélange de la vapeur d'eau, QV

-  Température de point de rosée, TD

-  Écart du point de rosée, ES

\*Résultat(s):\*

-  Indice humidex, HMX (scalaire, sans unité)

\*Algorithme:\*

.. code:: example

    Soit TTC la température de l'air à la surface [deg C]
    1) Calculer TD avec le plugin TemperatureDewPoint.
    2) Soit es(TD), la pression partielle de la vapeur [Pa] à saturation. Celle-ci peut être calculée avec le plugin SaturationVapourPressure en utilisant TD au lieux de TTC avec l'option --iceWaterPhase WATER

    On calcule ensuite l'humidex:

    HMX = TTC + (0.5555) * (es(TD) - 10)
    Si HMX > TTC
       resultat = HMX
    Sinon
       resultat = TTC

**Références:**

`Description of the humidex by
ECCC <http://ec.gc.ca/meteo-weather/default.asp?lang=En&amp;n=6C5D4990-1#humidex>`__

`Scribe
specifications <https://wiki.cmc.ec.gc.ca/images/0/0d/SITS14_specs.pdf>`__

**Mots clés:**

-  MÉTÉO/WEATHER, température/temperature, Humidité/humidité

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std] >>
                [Humidex] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Agnieszka
   Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Codé par : `Philippe
   Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à `Humidex <Humidex_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
