Français
--------

**Description:**

-  Ajoute un nombre donné à chaque élément d'un champ

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Le champ météorologique dont chaque élément est additionné de la
   valeur donnée

\*Algorithme:\*

example::

    Soit F, un champ de n éléments

    Soit z, une valeur donnée par la clé "value"

    Pour chaque point faire

        F(n) = F(n) + z        n >= 1

    Fin faire

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, ajout/add

\*Usage:\*

**Exemple d'appel:**

example::

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddToElement/testsFiles/inputFile.std] >>
                [AddToElement --value 1 ] >>
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

`Tests unitaires <AddToElementTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

English
-------

**Description:**

-  Add a given number to each element of a field

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field

\*Result(s):\*

-  The meteorological field to which the given value has been added to
   each element

\*Algorithm:\*

example::

    For F, a field of n elements

    For z, a value given by the "value" key

    for each point do

        F(n) = F(n) + z        n >= 1

    end do

**Reference:**

-  Does not apply

\*Keywords:\*

-  UTILITAIRE/UTILITY, ajout/add

\*Usage:\*

**Call example:**

example::

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AddToElement/testsFiles/inputFile.std] >>
                [AddToElement --value 1 ] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  

\*Contacts:\*

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

 

 
