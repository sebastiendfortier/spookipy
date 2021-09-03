Français
--------

**Description:**

-  Pour chaque élément d'un champ, verifie s'il y a une valeur nan

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  **Algorithme:**
-  **Références:**
-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/CheckNanValue/testsFiles/inputFile.std] >>
                [CheckNanValue] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

`Tests unitaires <CheckNanValueTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
