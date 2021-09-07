Français
--------

**Description:**

-  Lecture de fichier(s) standard(s) et conversion dans la structure de
   mémoire interne du système
-  Les informations associées à la représentation spatiale (aussi
   appelées "meta-informations"), sont lues automatiquement
-  `Le dictionnaire de variables
   standards <https://wiki.cmc.ec.gc.ca/wiki/Spooki/RelationsSpookiFSTD>`__
   est consulté lors de la lecture de chaque variable et l'unité
   correspondante est associée par défaut
   \*/Note :/\*si deux enregistrements identiques sont présents dans le
   fichier d'entrée, seul le premier sera retenu

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Un ou plusieurs fichier(s) standard(s) valide(s)
-  Note: L'heure de prévision est extraite à l'aide des descripteurs
   d'enregistrements DEET et NPAS et non directement à partir du
   descripteur d'enregistrement IP2

\*Résultat(s):\*

-  Fichiers standards fournis en entrée convertis en structure de
   mémoire interne

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  `Documentation sur les fichiers
   standards <https://wiki.cmc.ec.gc.ca/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_SPOOKI][Correspondance
   entre les descripteurs d'enregistrements de fichiers standards et les
   attributs de la mémoire interne de SPOOKI]]

\*Mots clés:\*

-  IO, lecteur/reader, decodeur/decoder, standard, fichier/file

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ReaderStd_WriterStd/testsFiles/inputFile.std] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Responsables:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
