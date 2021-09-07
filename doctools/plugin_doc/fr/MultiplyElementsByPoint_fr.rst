Français
--------

**Description:**

-  Multiplication en chaque point des valeurs de tous les champs reçus

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Au moins 2 champs différents

\*Résultat(s):\*

-  Un champ nommé "MUEP" avec le résultat de la multiplication des
   champs d'entrée.

\*Algorithme:\*

.. code:: example

    MUEP[i,j,k] = A[i,j,k] * B[i,j,k] * ...

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, grille/grid, point, multiplier/multiply,
   produit/product

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std] >>
                [MultiplyElementsByPoint] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests Unitaires

 
