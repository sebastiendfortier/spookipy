Français
--------

**Description:**

-  Calcul de la moyenne pondérée de l'humidité relative dans la basse
   troposphère et séparément dans la troposphère moyenne. Ceci est un
   produit pour l'aviation. Le calcul pour la basse troposphère utilise
   les niveaux à 1000, 925 et 850 hPa tandis que celui pour la
   troposphère moyenne utilise ceux à 850, 700 et 500 hPa.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Humidité spécifique, HU, à 1000, 925, 850, 700 et 500 hPa
-  Température, TT, à 1000, 925, 850, 700 et 500 hPa

\*Résultat(s):\*

-  Humidité relative, HR (fraction)

\*Algorithme:\*

.. code:: example

    Soit HU1000, HU925, HU850, HU700 et HU500, l'humidité spécifique (kg/kg) à 1000, 925, 850, 700 et 500 hPa respectivement.
    Soit HUs1000, HUs925, HUs850, HUs700 et HUs500, l'humidité spécifique saturante (kg/kg) à 1000, 925, 850, 700 et 500 hPa respectivement.
    Soit HRL, l'humidité relative de la basse troposphère et HRM, l'humidité relative de la troposphère moyenne.

    HRL = (HU1000 + 2*HU925 + HU850) / (HUs1000 + 2*HUs925 + HUs850)

    HRM = (HU850 + 2*HU700 + HU500) / (HUs850 + 2*HUs700 + HUs500)

    L'humidité spécifique saturante (HUs) se calcule en remplacant le champ TD (température du point de rosée) par TT dans le plugin HumiditySpecific.

    L'usager peut utiliser la clé --capped pour limiter la valeur la plus haute du résultat HR.

**Références:**

-  Non applicable

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature, humidité/humidity,
   pondéré/weighted

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HumidityRelativeWeightedMean/testsFiles/inputFile.std] >>
                [HumidityRelativeWeightedMean] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Codé par : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

`Tests unitaires <HumidityRelativeWeightedMeanTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
