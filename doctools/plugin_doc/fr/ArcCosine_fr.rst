Français
--------

**Description:**

-  applique la fonction : ACOS :math:` cos^{-1}z `

\*Méthode d'itération:\*

-  point par point

\*Dépendances:\*

-  un champ météorologique

\*Résultat(s):\*

-  le champ météorologique passé en entrée modifié

\*Algorithme:\*

-  pour chaque point applique l'algorithme choisi

\*Références:\*

-  man 3 acosf

\*Mots clés:\*

-  UTILITAIRE/UTILITY, inverse, cosinus/cosine

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArcCosine/testsFiles/inputFile.std] >>
                [ArcCosine --noFieldNameTag] >>
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

 
