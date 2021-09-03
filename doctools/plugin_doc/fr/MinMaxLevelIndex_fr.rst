Français
--------

**Description:**

-  Trouve l'indice de la valeur maximale et/ou minimale dans une
   colonne, ou une partie de celle-ci.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Champ météorologique (3D)
   **Si** la clé --bounded est activée:
-  Champ d'indices de la limite inférieure, KBAS (2D)
-  Champ d'indices de la limite supérieure, KTOP (2D)

\*Résultat(s):\*

-  Le champ météorologique (3D) reçu en entrée
-  Un champ d'indices, KMIN(2D), pour lesquels la valeur du champ
   météorologique est minimale
   **et/ou**
-  Un champ d'indices, KMAX(2D), pour lesquels la valeur du champ
   météorologique est maximale

\*Algorithme:\*

.. code:: example

    Si la clé --bounded n'est pas activée:
        KBAS = niveau le plus bas de la colonne
        KTOP = niveau le plus haut de la colonne

    Pour chaque colonne et pour les niveaux avec l'indice entre KBAS et KTOP

        Si la clé --minMax = MIN ou BOTH
            Boucle k = KBAS à KTOP
            Si min > VAR[k] alors min= VAR[k] et KMIN=k

        Si la clé --minMax = MAX ou BOTH
            Boucle k = KBAS à KTOP
            Si max < VAR[k] alors max = VAR[k] et KMAX=k

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, minimum, maximum, niveau/level, vertical,
   borné/bounded

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std] >>
                [MinMaxLevelIndex --minMax MIN --direction UPWARD] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

==

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std] >>
                ( [Copy] + ( ([SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName KBAS]) + ([SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName KTOP]) ) ) >>
                [MinMaxLevelIndex --bounded --minMax MIN --direction DOWNWARD] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Responsables:**

-  Auteur(e) : Daniel Figueras, `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__, Jonathan
   Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
