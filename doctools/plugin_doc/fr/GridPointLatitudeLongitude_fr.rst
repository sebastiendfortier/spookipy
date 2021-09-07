Français
--------

**Description:**

-  Sortie des latitudes et longitudes pour chaque point d'une grille.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ sur une grille

\*Résultat(s):\*

-  LA, latitude de chaque point de la grille donnée
-  LO, longitude de chaque point de la grille donnée

\*Algorithme:\*

    -  Appelle les routines de la librairie EZSCINT appropriées
    -  Retourne les latitudes et longitudes des points de la grille

**Références:**

-  `Librairie EZSCINT de
   RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint>`__

\*Mots clés:\*

-  GRILLE/GRID, point, latitude, longitude

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd         --input $SPOOKI_DIR/pluginsRelatedStuff/GridPointLatitudeLongitude/testsFiles/inputFile.std] >>
                [GridPointLatitudeLongitude] >>
                [WriterStd         --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
