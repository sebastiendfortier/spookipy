Français
--------

**Description:**

-  Vérifie si le nombre de niveaux d'un ou plusieurs champ(s) satisfait
   un des critères suivants :

   -  nombre égal au nombre de niveaux spécifié
   -  nombre inférieur ou égal au nombre maximum de niveaux spécifié
   -  nombre supérieur ou égal au nombre minimum de niveaux spécifié
   -  nombre de niveaux identique pour tous les champs entrés
   -  nombre de niveaux identique pour chaque grille entrée

\*Méthode d'itération:\*

-  Ne s'applique pas.

\*Dépendances:\*

-  Au moins un champ

\*Résultat(s):\*

-  Le résultat est affiché dans la sortie standard (STDOUT).
   ***Note:*** Aucune donnée ne sort de ce plugin.

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  SYSTÈME/SYSTEM, niveau/level, mimimum, maximum, exact, identique/same

\*Usage:\*

| ***Note:***

-  Une seule clé paramétrable doit obligatoirement être choisie parmi la
   liste.

\*Exemple d'appel:\*

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/CheckNumberOfLevels/testsFiles/inputFile.std] >>
                [CheckNumberOfLevels --minimum 1] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
-  Codé par : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
