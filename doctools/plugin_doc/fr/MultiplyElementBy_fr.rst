Français
--------

**Description:**

-  Multiplication de chaque élément d'un champ par une valeur donnée

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Le champ météorologique dont chaque élément est multiplié par la
   valeur donnée

\*Algorithme:\*

.. code:: example

    Soit F, un champ de n éléments

    Soit z, une valeur donnée par la clé "value"

    Pour chaque point faire

        F(n) = F(n) *  z        n >= 1

    Fin faire

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, multiplier/multiply

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std] >>
                [MultiplyElementBy --value 10] >>
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

`Tests unitaires <MultiplyElementByTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
