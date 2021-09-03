Français
--------

**Description:**

-  Calcul de l'épaisseur entre deux niveaux d'un champ de hauteur
   géopotentielle donné.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Un champ de hauteur géopotentielle, GZ (au moins 2 niveaux)

\*Résultat(s):\*

-  Champ d'épaisseur, DZ (mêmes unités que la source)

\*Algorithme:\*

.. code:: example

    Vérifie que le type de coordonnée verticale du champ d'entrée correspond bien à la clé "coordinateType" passée en paramètre
    si oui, va chercher dans le champ d'entrée, à l'aide du plugin Select, les niveaux passés en paramètre et faire en chaque point:
        DZ = ABS ( GZ(top) - GZ(base) )
    sinon
        sortir du plugin avec un message d'erreur
    fin si

**Références:**

-  Non applicable

\*Mots clés:\*

-  MÉTÉO/WEATHER, épaisseur/thickness, hauteur/height,
   géopotentielle/geopotential, niveau/level, différence/difference

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Thickness/testsFiles/inputFile.std] >>
                [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
