Français
--------

**Description:**

-  prend la valeur decodé du ip1 - soit le niveau - et le place dans le
   champ

\*Méthode d'itération:\*

-  Niveau par niveau

\*Dépendances:\*

-  un champ météorologique

\*Résultat(s):\*

-  un champ dont chaque point a la valeur de son niveau

\*Algorithme:\*

-  A[i, j, k] = convip(ip1[K])

\*Références:\*

-  N.D.

\*Mots clés:\*

-  UTILITAIRE/UTILITY, ip1, niveau/level

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std] >>
                [LevelFromIp1] >>
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

Voir la référence à .

Tests Unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
