Français
--------

**Description:**

-  Détermine les indices des niveaux verticaux correspondants à la base
   et au sommet d'une variable météorologique, selon le seuil mentionné
   lors de l'appel.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  La variable météorologique (champ 3D)
-  Champ de l'indice du niveau vertical le plus bas de la variable
   météorologique (BASI)
-  Champ de l'indice du niveau vertical le plus haut de la variable
   météorologique (TOPI)

\*Résultat(s):\*

-  Indice du niveau vertical de la base (KBAS)
-  Indice du niveau vertical du sommet (KTOP)

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/f/ff/Spooki_-_Algorithme_BaseTop_v1.1.doc

\*Références:\*

-  Inspiré du programme opérationnel 'ecldcig:sub:`fstd2000`.f'
   https://wiki.cmc.ec.gc.ca/images/3/36/Spooki_-_Programme_Operationnel_CloudAmountAndLevel_Ecldcig_fstd2000.f

\*Mots clés:\*

-  UTILITAIRE/UTILITY, base, sommet/top

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/BaseTopBoundedLevelIndex/testsFiles/inputFile.std] >>
                [BaseTopBoundedLevelIndex --comparisonOperator >= --threshold 0.6] >>
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

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests Unitaires

 
