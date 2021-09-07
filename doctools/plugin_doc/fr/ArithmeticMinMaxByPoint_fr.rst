Français
--------

**Description:**

-  Trouver la valeur maximale et/ou minimale en chaque point de tous les
   champs disponibles sur la même grille

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Champs météorologiques sur la même grille

\*Résultat(s):\*

-  Un champ de valeurs, MIN
   **et/ou**
-  Un champ de valeurs, MAX

\*Algorithme:\*

    Soit des champs A (i,j,k), B (i,j,k), C(i,j,k), ....

    MIN(i,j,k) = min( A(i,j,k), B(i,j,k), C(i,j,k), ... )

    MAX(i,j,k) = max( A(i,j,k), B(i,j,k), C(i,j,k), ... )

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, minimum, maximum

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMinMaxByPoint/testsFiles/inputFile.std] >>
                [ArithmeticMinMaxByPoint --minMax BOTH] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur : `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__
-  Codé par : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests Unitaires

 
