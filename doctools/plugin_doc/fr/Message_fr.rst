Français
--------

**Description:**

-  Affiche un message donné dans la sortie standard (STDOUT) lors de
   l'exécution

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Aucune

\*Résultat(s):\*

-  Le message est affiché dans la sortie standard (STDOUT).
   ***Note:*** Aucune donnée ne sort du plugin.

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  SYSTÈME/SYSTEM, message, STDOUT

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Message/testsFiles/inputFile.std] >>
                ( [Select --fieldName TT] || ([Copy] + [Message --severity WARNING --verificationMessage No_TT_found,_write_anyway]) ) >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à `Message <Message_8cpp.html>`__.

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
