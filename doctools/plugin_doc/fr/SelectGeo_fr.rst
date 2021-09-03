Français
--------

**Description:**

-  Permet de faire une sélection géographique dans un ensemble de
   données

\*Méthode d'itération:\*

-  N/D

\*Dépendances:\*

-  N/D

\*Résultat(s):\*

-  N/D

\*Algorithme:\*

-  N/D

\*Références:\*

-  N/D

\*Mots clés:\*

-  SYSTÈME/SYSTEM, sélection/selection, géographique/geographical,
   latitude, longitude

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [SelectGeo --longitude1 272.425 --latitude1 45.1621 --longitude2 278.816 --latitude2 46.6413] >>
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

Voir la référence à `SelectGeo <SelectGeo_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
