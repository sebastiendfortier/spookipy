Français
--------

**Description:**

-  Opération logique qui retourne toujours vrai.

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Aucune

\*Résultat(s):\*

-  Retourne vrai au système (opération système)
   ***Note:*** Aucune donnée ne sort du plugin

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  SYSTÈME/SYSTEM, logique/logical, vrai/true

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                ( [TrueOperation] + [Copy] || [FalseOperation] ) >>
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

Voir la référence à

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
