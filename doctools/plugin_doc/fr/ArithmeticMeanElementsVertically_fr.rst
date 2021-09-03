Français
--------

**Description:**

-  Moyenne arithmétique dans la verticale de chaque champ donné en
   entrée

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Au moins un champ 3D

\*Résultat(s):\*

-  Champ(s) 2D moyenné(s) dans la verticale, de même nom(s) que
   celui(ceux) donné(s) en entrée

\*Algorithme:\*

    Soit F , un champ de N niveaux, de valeurs F(k), k=1,N dans la
    verticale

    Pour chaque colonne:

    :math:`\mbox{ $F = \frac {\sum_{k=0}^{N} F(k)}{N+1}$}`

**Références:**

-  Aucune

\*Mots clés:\*

-  UTILITAIRE/UTILITY, moyenne/mean, verticale/vertical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMeanElementsVertically/testsFiles/inputFile.std] >>
                [ArithmeticMeanElementsVertically] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

| \*Ce plugin utilise:\*
| **Ce plugin est utilisé par:**
| Voir la référence à

Tests unitaires

 
