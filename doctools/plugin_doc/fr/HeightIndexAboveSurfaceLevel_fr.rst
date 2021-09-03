Français
--------

**Description:**

-  Permet d'obtenir l'indice du niveau du champ GZ qui est >= à la
   hauteur fournie en paramètre par rapport au sol. Utiliser
   MatchLeveIndiceToValue pour obtenir la valeur correspondant à
   l'indice.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Hauteur géopotentielle GZ

\*Résultat(s):\*

-  Champ IND 2D contenant les indices trouvés

\*Algorithme:\*

-  Trouver k où Hauteur >= GZ[k] - GZ[0]

\*Références:\*

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, hauteur/height, géopotentiel/geopotential

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/HeightIndexAboveSurfaceLevel/testsFiles/inputFile.std] >>
                [HeightIndexAboveSurfaceLevel --height 3 --unit kilometer] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
