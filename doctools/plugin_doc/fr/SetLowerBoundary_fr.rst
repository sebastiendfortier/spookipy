Français
--------

**Description:**

-  Borner le minimum d'un champ à la valeur spécifiée.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Un champ météorologique dont aucune valeur n'est inférieure à la
   valeur spécifiée

\*Algorithme:\*

.. code:: example

    Soit F, un champ donné de dimension N, composé de n éléments (n =1, N)

    Soit z, une valeur donnée par la clé "value", désignée comme borne inférieure du champ F

    Pour chaque point n=1,N faire

        Si F(n) < z alors
           F(n) = z
        Finsi

    Fin faire

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, minimum, borne/bound, inférieur/lower

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetLowerBoundary/testsFiles/inputFile.std] >>
                [SetLowerBoundary --value 1 ] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
