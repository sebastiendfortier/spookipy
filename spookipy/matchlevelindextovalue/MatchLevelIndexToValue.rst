Français
--------

**Description:**

-  Associe, à chaque indice de niveau vertical donné, la valeur d'un ou
   de plusieurs champ(s) météorologique(s) 3D donné(s) en entrée.
   ***Note:*** La numérotation des indices des niveaux verticaux
   commence à zéro

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Un champ d'indices de niveaux verticaux, IND (2D)
-  Un ou plusieurs champ(s) météorologique(s) (3D)

\*Résultat(s):\*

-  Champ(s) météorologique(s) (2D) dont les valeurs correspondent à
   celles des niveaux verticaux spécifiés par le champ d'indices IND

\*Algorithme:\*

.. code:: example

    Soit IND, un champ 2D d'indices de niveaux verticaux dont la numérotation des indice commence à 0.

    Pour chaque champ météorologique 3D, CHP3D, donné en entrée, faire :
        Pour chaque i,j
            CHP2D(i,j) = CHP3D(i,j,IND(i,j))
        Fin boucle sur les points
    Fin boucle sur les champs

**Références:**

-  N/D

\*Mots clés:\*

-  UTILITAIRE/UTILITY, associer/match, niveau/level, vertical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MatchLevelIndexToValue/testsFiles/inputFile.std] >>
                [MatchLevelIndexToValue] >>
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

 

English
-------

**Description:**

-  Associates, to each vertical level index given, a value of one or
   many 3D meteorological fields given in input.
   ***Note:*** The numbering of the indices starts at zero

\*Iteration method:\*

-  Column by column

\*Dependencies:\*

-  A field of vertical level indexes, IND (2D)
-  One or many meteorological field(s) (3D)

\*Result(s):\*

-  Meteorological field(s) (2D) which the values correspond to those of
   the vertical levels specified by the index field IND

\*Algorithm:\*

.. code:: example

    For IND, a 2D field of vertical level indexes, where the index numbering starts at 0.

    For each 3D meteorological field, CHP3D, given in input, do :
        For each i,j
            CHP2D(i,j) = CHP3D(i,j,IND(i,j))
        End loop on i,j
    End loop on the fields

**Reference:**

-  None

\*Keywords:\*

-  UTILITAIRE/UTILITY, associer/match, niveau/level, vertical

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MatchLevelIndexToValue/testsFiles/inputFile.std] >>
                [MatchLevelIndexToValue] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
