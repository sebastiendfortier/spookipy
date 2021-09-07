Français
--------

**Description:**

-  Somme en chaque point des valeurs de tous les champs reçus.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Au moins 2 champs différents

\*Résultat(s):\*

-  Un champ nommé "ADEP" avec le résultat de la somme des champs
   d'entrée

\*Algorithme:\*

-  ADEP[i,j,k] = A[i,j,k] + B[i,j,k] + ...

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, accumuler/accumulate, ajout/add, somme/sum

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddElementsByPoint/testsFiles/inputFile.std] >>
                [AddElementsByPoint] >>
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

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests Unitaires

English
-------

**Description:**

-  Add, for each point, the values of all the fields received

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  At least 2 different fields

\*Result(s):\*

-  A field named "ADEP" with the result of the sum of the fields
   received from input

\*Algorithm:\*

-  ADEP[i,j,k] = A[i,j,k] + B[i,j,k] + ...

\*Reference:\*

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, accumuler/accumulate, ajout/add, somme/sum

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddElementsByPoint/testsFiles/inputFile.std] >>
                [AddElementsByPoint] >>
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

 

 