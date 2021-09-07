Français
--------

**Description:**

-  Convertit toutes les données reçues dans une unité compatible
-  La liste de toutes les unités valides est disponible
   `ici <units.html>`__
-  Possibilité de convertir les données reçues dans des unités définies
   par défaut dans la `base de données des variables des fichiers
   standard <stdvar.html>`__

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Champ avec unité valide

\*Résultat(s):\*

-  Champ en entrée converti dans une unité compatible donnée

\*Algorithme:\*

.. code:: example

    Applique le facteur de conversion à chaque donnée
    Si l`unité "STD" est choisie,
        Toutes les données sont converties à l`aide des unités compatibles décrites dans la base de données des variables des fichiers standard
        Si le champ n`existe pas dans la base de données, le plugin arrête et avertit l`utilisateur, sauf si la clé "--ignoreMissing" est activée, dans ce cas, aucune conversion n`est effectuée

**Références:**

-  `Base de données des unités <units.html>`__
-  `Base de données des variables <stdvar.html>`__

\*Mots clés:\*

-  SYSTÈME/SYSTEM, unité/unit, convertir/convert

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/UnitConvert/testsFiles/inputFile.std] >>
                [UnitConvert --unit kilometer_per_hour] >>
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

 
