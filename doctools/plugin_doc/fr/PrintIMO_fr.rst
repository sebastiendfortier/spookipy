Français
--------

**Description:**

-  Ce plugin sert à des fins de débogage et imprime le contenu de la
   stucture mémoire (IMO).

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Un champ dans la structure interne de mémoire.

\*Résultat(s):\*

-  Ne s'applique pas

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  `Composantes de la structure interne de
   mémoire <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_système#meteo_infos>`__

\*Mots clés:\*

-  SYSTÈME/SYSTEM, impression/print, mémoire/memory, débogage/debugging

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [PrintIMO  --output /tmp/$USER/outputFile.txt --extended]"
    ...

Note: La clé --output Permet d'écrire le contenu de la structure mémoire
(IMO) dans le fichier de sortie. La clé --extended Si la clé n'est pas
utilisée, seulement un sous-ensemble de la structure mémoire sera
affichée.

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à `PrintIMO <PrintIMO_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
