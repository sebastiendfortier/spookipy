Français
--------

**Attention! Plugin à usage restreint**
=======================================

**Description:**

-  Lecture de fichier de format CSV (valeurs séparées par des virgules)
   et conversion dans la structure de mémoire interne du système

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Un fichier avec valeurs separées par des virgules

\*Résultat(s):\*

-  Fichier CSV fourni en entrée converti en structure de mémoire interne

\*Algorithme:\*

-  | Lecture d'un fichier qui doit avoir la forme suivante:

   .. code:: example

       gds:typeOfGeographicalProjection,IP1,IP2,IP3 # section gds

       pds:fieldName,pdsLabel   # première section pds

       level:float              # premier niveau
       float,float,...,float    # ---
       float,float,...,float    # - section matrice
       ...                      # - de données
       float,float,...,float    # ---

       level:float              # deuxième niveau
       float,float,...,float    # ---
       float,float,...,float    # - section matrice
       ...                      # - de données
       float,float,...,float    # ---

       pds:fieldName2,pdsLabel  # deuxième section pds
       ...

       - Le charactère # indique un commentaire
       - On peut avoir plusieurs sections pds mais une seule section gds.
       - Chacune des sections pds peut contenir plusieurs niveaux.
       - Le nombre de lignes d'une section matrice détermine la taille en x
         de la matrice dans la structure interne de mémoire.
       - Le nombre de colonnes d'une section matrice détermine la taille en y
         de la matrice dans la structure interne de mémoire.

   Exemple du contenu d'un fichier CSV:
   gds:TYPE\ :sub:`X`,6,7,8
   pds:F1,ETIKET
   level:1.0
   11.1,22.2
   33.3,44.4
   55.5,66.6
   level:0.0
   77.7,88.8
   99.9,100.10
   110.11,120.12
   pds:F2,ETIKET
   level:99.0
   1.2,2.3,3.4
   4.5,5.6,6.7
-  voir les fichiers .csv dans le répertoire
   $SPOOKI\ :sub:`DIR`/pluginsRelatedStuff/ReaderCsv/miscellaneous pour
   des exemples.

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  IO, lecteur/reader, decodeur/decoder, csv, fichier/file

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderCsv --input   $SPOOKI_DIR/pluginsRelatedStuff/ReaderCsv/testsFiles/inputFile.csv] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Responsables:**

-  Auteur(e) : François Fortin
-  Codé par : François Fortin
-  Support : CMDW / CMDS

Voir la référence à `ReaderCsv <ReaderCsv_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
