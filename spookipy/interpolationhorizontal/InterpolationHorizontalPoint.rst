Français
--------

**Description:**

-  Interpolation horizontale d'un ou plusieurs champ(s) sur un ensemble
   de points de latitudes et longitudes données.
-  Les champs peuvent être scalaires (ex: température) ou vectoriels
   (ex: vent horizontal).
   ***Note:*** : Seul le vent peut être interpolé vectoriellement.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un ou plusieurs champ(s) sur une ou plusieurs grille(s) source(s)
-  Un champ destination de latitudes (LAT), en degrés décimaux signés
-  Un champ destination de longitudes (LON), en degrés décimaux signés

\*Résultat(s):\*

-  Un ou plusieurs champ(s) interpolé(s) sur un certain nombre de points
   de latitudes et de longitudes données

\*Algorithme:\*

-  Détecte la nature scalaire ou vectorielle des champs entrés sur la
   grille source
-  Appelle les routines scalaires ou vectorielles de la librairie
   EZSCINT selon la nature des champs et des clés paramétrables
-  Retourne les champ interpolés aux points, de latitudes et longitudes
   données

\*Références:\*

-  `Librairie EZSCINT de
   RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

\*Mots clés:\*

-  INTERPOLATION, extrapolation, horizontale/horizontal, point, ezscint

\*Usage:\*

\*/\ `Notes:/\*\\\\ <Notes:/*\\>`__ Pour la clé "--interpolationType":

-  NEAREST: la valeur interpolée en un point de latitude et longitude
   données est obtenue par la valeur du point le plus proche de la
   grille source.
-  BI-LINEAR: interpolation bi-linéaire.
-  BI-CUBIC: interpolation bi-cubique.

Pour la clé "--extrapolationType":

-  MAXIMUM: les valeurs à l'extérieur du domaine sont remplacées par la
   valeur maximum du champ à laquelle est ajouté 5% de sa variation
   totale.
-  MINIMUM: les valeurs à l'extérieur du domaine sont remplacées par la
   valeur minimum du champ à laquelle est soustrait 5% de sa variation
   totale.
-  VALUE: les valeurs à l'extérieur du domaine sont remplacées par une
   valeur numérique donnée (float).
-  ABORT: abandon de la requête.

\*Exemple d'appel:\*

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.std] >>
                [ReaderCsv --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.csv] >>
                [InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

-  `Autres
   exemples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Exemples#Exemples_d.27interpolation_horizontale_sur_un_ensemble_de_points_de_latitudes_et_longitudes_donn.C3.A9es>`__

\*Validation des résultats:\*

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**
|  

English
-------

**Description:**

**Iteration method:**

-  N/A

\*Dependencies:\*

-  N/A

\*Result(s):\*

-  N/A

\*Algorithm:\*

-  N/A

\*References:\*

-  N/A

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  INTERPOLATION, extrapolation, horizontale/horizontal, point, ezscint

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.std] >>
                [ReaderCsv --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalPoint/testsFiles/inputFile.csv] >>
                [InterpolationHorizontalPoint --interpolationType BI-LINEAR --extrapolationType VALUE=99.9] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  Under construction!

\*Contacts:\*

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
