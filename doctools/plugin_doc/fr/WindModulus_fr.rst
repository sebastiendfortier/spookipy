Français
--------

**Description:**

-  Calcul du module du vent à partir de ses 2 composantes horizontales.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Composante UU du vent (selon l'axe des X sur la grille).
-  Composante VV du vent (selon l'axe des Y sur la grille).

\*Résultat(s):\*

-  Module du vent, UV, dans les mêmes unités que ses dépendances.

\*Algorithme:\*

-  Appelle le plugin
   `WindModulusAndDirection <pluginWindModulusAndDirection.html>`__.
-  Le vent étant un vecteur avec 2 composantes, appelle le plugin
   `VectorModulusAndDirection <pluginVectorModulusAndDirection.html>`__
-  Conserve uniquement le résultat du module, MOD, dans la variable UV.

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  MÉTÉO/WEATHER, module/modulus, vent/wind, vitesse/speed

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std] >>
                [WindModulus] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
