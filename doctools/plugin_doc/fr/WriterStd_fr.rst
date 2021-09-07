Français
--------

**Description:**

-  Ecriture de données dans un fichier en format RPN standard
-  Convertit par défaut, chaque variable dans l'unité correspondant au
   `dictionnaire de variables
   standards. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/RelationsSpookiFSTD>`__

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Données dans la mémoire interne du système SPOOKI (PDS)

\*Résultat(s):\*

-  Un ou des enregistrement(s) encodé(s) dans un fichier en format RPN
   standard
-  Les enregistrements sont triés et écrits dans l'ordre suivant :
   meta-informations, ordre alphabétique de noms de variables, ordre de
   niveaux (de bas en haut), ordre temporel
-  Les valeurs de IP2 et IP3 ne sont pas encodées et IP3 contient le
   delta de l'interval.

\*Algorithme:\*

-  Avec l'aide du tableau sur la page de correspondance entre les
   `fichiers standards et
   SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_SPOOKI>`__,
   ce plugin transfère (écrit) l'information des attributs de la mémoire
   interne de SPOOKI aux descripteurs d'enregistrement des fichiers
   standards en suivant `les règles
   suivantes <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Tableau_r%C3%A8gles_pour_WriterStd>`__.
-  Convertit chaque variable vers son unité standard tel que désignée
   par `le dictionnaire de variables
   standards <http://iweb.cmc.ec.gc.ca/~afsypst/spooki/spooki_french_doc/html/stdvar.html>`__,
   à l'aide du plugin , sauf si la clé "--noUnitConversion" est activée.
   Lors de cette conversion, le deuxième caractère du TYPVAR n'est pas
   affecté. Si l'unité d'origine n'est pas connue, la conversion ne peut
   avoir lieu, le plugin arrête en indiquant: "L'unité n'est pas connue,
   si vous désirez écrire la variable avec l'unité d'origine, utilisez
   la clé &ndash;noUnitConversion."
-  Trie les variables selon l'ordre désigné par le système
   (meta-informations, ordre alphabétique de noms de variables, ordre de
   niveaux (de bas en haut), ordre temporel).
-  Si la clé "--noMetadata" est activée, ne copie pas les
   "meta-informations" (informations associées à la représentation
   spatiale: enregistrements ">>","^^","HY","P0","PT","E1","!!","!!SF").
-  Si la clé "--metadataOnly" est activée, copie seulement les
   "meta-informations" (informations associées à la représentation
   spatiale: enregistrements ">>","^^","HY","P0","PT","E1","!!","!!SF").
-  Ce plugin écrit au fichier nommé par l'argument donné à la clé
   "--output". Si ce fichier existe déjà, par défaut (option
   APPENDOVERWRITE de la clé "--writingMode"), on écrit par dessus les
   enregistrements qui ont les mêmes valeurs dans les descripteurs
   d'enregistrements que les nouvelles données et on garde les autres
   données déjà dans le fichier. Si on choisit l'option NOPREVIOUS de la
   clé "--writingMode" et que le fichier existe déjà, le plugin arrête
   avec un message approprié. Si on choisit l'option NEWFILEONLY, on
   efface le fichier et on crée un nouveau fichier contenant
   exclusivement les nouvelles données.
-  Important: Si le fichier (dans l'argument de --output) existe déjà et
   que ce fichier n'est pas un fichier standard, la requête arrête
   indiquant que le fichier dans l'argument de --output existe déjà et
   n'est pas de type standard. On invite ensuite l'usager à résoudre le
   conflit avant de relancer SPOOKI.
-  Le fichier final ne contient pas deux champs distincts de "HY" ou de
   "!!". Pour les "^^" et ">>", des champs distincts sont permis sauf
   s'ils ont les mêmes IP1 et IP2 mais pas les mêmes IG1,IG2,IG3 et IG4.
   Si un deuxième "HY" ou "!!" distincts ou des champs "^^" et ">>"
   distincts non-permis existent dans les données à écrire et/ou le
   fichier d'écriture, la requête arrête avec un message claire
   expliquant le problème.

\*Références:\*

-  `Documentation sur les fichiers
   standards <https://wiki.cmc.ec.gc.ca/images/8/8c/Spooki_-_An_Introduction_to_RPN_Standard_files.pdf>`__
-  `Tableau de comparaison entre les fichiers standards et
   SPOOKI <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_SPOOKI>`__

\*Mots clés:\*

-  IO, standard, graveur/writer, fichier/file

\*Usage:\*

    | ***Notes: Pour la clé "--writingMode":***

    -  NOPREVIOUS: Le plugin arrête si le fichier standard existe déjà.
    -  APPEND : Si le fichier standard existe déjà , on rajoute tous les
       enregistrements dans la mémoire disponible aux plugin.
    -  APPENDOVERWRITE: Si le fichier standard existe déjà, on écrit par
       dessus les enregistrements qui ont les mêmes valeurs dans les
       descripteurs d'enregistrement que les nouvelles données et on
       garde les autres données déjà dans le fichier. (Mode par défaut)
    -  NEWFILEONLY: Si le fichier standard existe déjà, on efface le
       fichier et on crée un nouveau fichier contenant exclusivement les
       nouvelles données.

    \*Exemple d'appel:\*

    .. code:: example

        ...
            spooki_run "[ReaderStd --input  $SPOOKI_DIR/pluginsRelatedStuff/ReaderStd_WriterStd/testsFiles/inputFile.std] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Responsables:**

    -  Auteur(e) : `François
       Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Luc
       Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
    -  Codé par : `François
       Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ `Luc
       Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à `WriterStd <WriterStd_8cpp.html>`__.

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
