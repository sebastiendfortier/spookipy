Français
--------

**Description:**

-  Calcule la racine carrée de chaque élément d'un champ donné

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Le champ météorologique dont la valeur à chaque point est la racine
   carrée du champ entré.

\*Algorithme:\*

-  Applique la fonction :math:` \sqrt{z} ` à chaque valeur (z) du champ
   donné

\*Références:\*

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, racine/root, carré/square, point

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SquareRoot/testsFiles/inputFile.std] >>
                [SquareRoot --noFieldNameTag] >>
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

`Tests unitaires <SquareRootTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
