Français
--------

**Description:**

-  Copie du champ d'entrée sans modification

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Au minimum un champ en entrée

\*Résultat(s):\*

-  Le même champ qu'en entrée

\*Algorithme:\*

-  A[i,j,k] = A[i,j,k]

\*Références:\*

-  Aucune

\*Mots clés:\*

-  SYSTÈME/SYSTEM, copie/copy, logique/logical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Copy/testsFiles/inputFile.std] >>
                ( [Copy] + [Message --severity WARNING --verificationMessage copy_of_input] ) >>
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

Voir la référence à `Copy <Copy_8cpp.html>`__.

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
