Français
--------

**Description:**

-  Ce plugin sert des fins de débogage et imprime le contenu de la
   stucture mémoire (IMO).

\*Méthode d'itration:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Un champ dans la structure interne de mémoire.

\*Résultat(s):\*

-  Ne s'applique pas

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  `Composantes de la structure interne de
   mémoire <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_systme#meteo_infos>`__

\*Mots clés:\*

-  SYSTÈME/SYSTEM, impression/print, mémoire/memory, débogage/debugging

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [Print  --output /tmp/$USER/outputFile.txt --outputType VOIR]"
    ...

Note: La clé --output Permet d'écrire le contenu de la structure mémoire
(IMO) dans le fichier de sortie. La clé --outputType Formatte la les
donnes dans le style de l'outil sélectionné.

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la rfrence `Print <Print_8cpp.html>`__.

Tests unitaires

|image0|

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 

.. |image0| image:: Print_graph.png

