Français
--------

**Attention! Plugin à usage restreint**
=======================================

**Description:**

-  Fusion de toutes les grilles similaires reçues par le plugin.
-  Deux grilles sont similaires quand leur type de projection ainsi que
   leur taille en X et en Y sont identiques.
-  Si au moins une grille n'est pas similaire aux autres grilles
   disponibles, le plugin échoue.

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Au minimum un champ en entrée

\*Résultat(s):\*

-  Tout les champs sur une seule grille.

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, grille/grid, similaire/similar, merge/fusion

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/GridMergeSimilar/testsFiles/inputFile.std] >>
                [GetDictionaryInformation --dataBase STATIONS --table STATIONSFB --outputAttribute FictiveStationFlag ] >>
                [GridMergeSimilar] >> [PrintIMO]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
