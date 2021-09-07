Français
--------

**Description:**

-  Vérifier si les valeurs d'un champ sont à l'intérieur d'un écart
   donné

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ en entrée

\*Résultat(s):\*

-  Un champ de même taille que celui en entrée et portant le même nom
   suivi d'une asterix et contenant des valeures booléenne indiquant si
   la valeur est contenue dans l'écart

\*Algorithme:\*

-  IN étant le champ en entrée, pour chaque point on retourne (IN[i,j,k]
   >= min) and (IN[i,j,k] <= max)

\*Références:\*

-  Aucune

\*Mots clés:\*

-  SYSTÈME/SYSTEME, check

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/CheckRange/testsFiles/inputFile.std] >>
                [CheckRange --range 1@2] >>
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

Voir la référence à `CheckRange <CheckRange_8cpp.html>`__.

Tests Unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
