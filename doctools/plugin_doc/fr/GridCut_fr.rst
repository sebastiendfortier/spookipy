Français
--------

**Description:**

-  Permet de découper un morceau de grille, défini par son point
   supérieur gauche et son point inférieur droit.

       \*/\ Notes:/* Ce plugin permet de créer une grille complètement
       autonome S'il est désiré de fusionner plusieurs grilles, ces
       grilles doivent avoir été découpées par ce plugin dans la même
       exécution de Spooki

\*Méthode d'itération:\*

-  Point par point.

\*Dépendances:\*

-  Un ou plusieurs champ(s) sur une ou plusieurs grille(s) source(s)

\*Résultat(s):\*

-  Les champs en entrée sur un morceau de grille, avec les mêmes
   métadonnées qu'en entrée.

\*Algorithme:\*

-  Les grilles d'entrée sont référencées, ainsi que leurs données et
   leurs descripteurs
-  Les grilles de sortie sont créées en copiant les paramètres des
   grilles d'entrée et en modifiant les dimensions
-  Les données désirées sont copiées.

\*Références:\*

-  N/D

\*Mots clés:\*

-  SYSTÈME/SYSTEM, grille/grid, découpage/cut, sélection/select

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/GridCut/testsFiles/inputFile.std] >>
                [GridCut --startPoint 5,16 --endPoint 73,42] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Maximilien
   Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__
-  Codé par : `Maximilien
   Martin <https://wiki.cmc.ec.gc.ca/wiki/User:Martinm>`__ `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à `GridCut <GridCut_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
