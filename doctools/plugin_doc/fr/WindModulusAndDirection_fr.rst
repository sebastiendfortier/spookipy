Français
--------

**Description:**

-  Calcul du module et de la direction du vent.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Composante UU du vent (selon l'axe des X).
-  Composante VV du vent (selon l'axe des Y).

\*Résultat(s):\*

-  Module du vent, UV, dans les mêmes unités que ses dépendances.
-  Direction météorologique du vent, WD (deg).

\*Algorithme:\*

-  Le vent étant un vecteur avec 2 composantes, appelle le plugin
   `VectorModulusAndDirection <pluginVectorModulusAndDirection.html>`__
   avec la clé paramétrable --orientationType WIND

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, module/modulus, direction, angle

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std] >>
                [WindModulusAndDirection] >>
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

 
