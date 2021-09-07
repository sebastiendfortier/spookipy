Français
--------

**Description:**

-  De la valeur d'un champ au niveau choisi (le plus haut ou le plus
   bas), soustraire les valeurs de tous les autres niveaux de ce champ.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Au moins un champ 3D

\*Résultat(s):\*

-  Un champ 2D du même nom que celui en entrée

\*Algorithme:\*

.. code:: example

    Soit k le niveau de départ chosi

    Si direction = "ASCENDING" alors
        A = A[k] - A[k+1] - A[k+2] - ...
    Sinon
        A = A[k] - A[k-1] - A[k-2] - ...
    Finsi

**Références:**

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, soustraire/subtract, soustraction/subtraction,
   verticale/vertical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SubtractElementsVertically/testsFiles/inputFile.std] >>
                    [SubtractElementsVertically --direction ASCENDING] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
      ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests Unitaires

 
