Français
--------

**Description:**

-  Applique la valeur absolue à chaque élément d'un champ

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Le champ météorologique en valeur absolue

\*Algorithme:\*

-  Applique la fonction \|z\| à chaque valeur (z) du champ donné

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, absolue/absolute

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AbsoluteValue/testsFiles/inputFile.std] >>
                [AbsoluteValue] >>
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

`Tests unitaires <AbsoluteValueTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
