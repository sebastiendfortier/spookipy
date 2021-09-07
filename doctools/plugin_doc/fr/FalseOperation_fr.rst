Français
--------

**Description:**

-  Opération logique qui retourne toujours faux

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Aucune

\*Résultat(s):\*

-  Retourne faux au système (opération système) et arrête l'exécution du
   programme.
   ***Note:*** Aucune donnée ne sort du plugin

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  SYSTÈME/SYSTEM, logique/logical, faux/false

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std] >>
                ( [Copy] || [FalseOperation] ) >>
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

Voir la référence à `FalseOperation <FalseOperation_8cpp.html>`__.

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
