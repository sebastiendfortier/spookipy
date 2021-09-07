Français
--------

**Description:**

-  Moyenne arithmétique en chaque point de tous les champs reçus

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Au moins 2 champs différents

\*Résultat(s):\*

-  La moyenne des champs fournis en entrée nommé "MEAN"

\*Algorithme:\*

    Soit N champs Fn , (n=1,n)

    La moyenne arithmétique des N champs fournis en entrée s'exprime en
    chaque point (i,j,k) selon :

    :math:`\mbox{ $MEAN(i,j,k) = \frac {\sum_{n=1}^{N} F_n(i,j,k)}{N}$}`

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, moyenne/mean, average

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ArithmeticMeanByPoint/testsFiles/inputFile.std] >>
                [ArithmeticMeanByPoint] >>
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

 
