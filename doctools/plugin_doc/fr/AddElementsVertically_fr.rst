Français
--------

**Description:**

-  Addition de toutes les valeurs d'un champ dans la verticale

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Au moins un champ 3D

\*Résultat(s):\*

-  Un champ 2D du même nom que celui en entrée

\*Algorithme:\*

.. code:: example

    Additionne colonne par colonne toutes les valeurs d'un champ dans la verticale :

    A = A[k] + A[k+1] + A[k+2] + ...

**Références:**

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, accumuler/accumulate, addition,
   verticale/vertical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddElementsVertically/testsFiles/inputFile.std] >>
                [AddElementsVertically] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests unitaires

 
