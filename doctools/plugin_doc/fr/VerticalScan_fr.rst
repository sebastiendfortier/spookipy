Français
--------

**Description:**

-  Recherche d'occurrence(s) dans la verticale de l'évènement A=B, où A
   provient du champ de référence et B du champ de comparaison. Selon la
   demande de l'utilisateur, le plugin calcule pour chaque occurence, la
   hauteur géopotentielle et/ou la pression associée(s) par
   interpolation linéaire dans les cas où A=B entre 2 niveaux donnés
   (interpolation en lnp si la sortie demandée est en pression). Si par
   ailleurs, A=B se produit sur le 1er niveau de l'échantillon, le
   plugin ne considère pas ce niveau et continue sa recherche à partir
   du niveau suivant. Advenant le cas où la clé --checkForEquality est
   utilisée, le plugin va considérer le 1er niveau où cette égalité se
   produit.
-  Une variable booléenne BOVS est créée pour donner une indication de
   la valeur comparative de A par rapport à B au 1er niveau de
   l'échantillon. Plus précisémment, BOVS=false (0) si A < B au plus bas
   niveau, et BOVS=true (1) inversement. Dans le cas où A=B au 1er
   niveau, c'est le niveau suivant qui va permettre de décider de la
   valeur de la variable logique: si le niveau suivant est tel que A < B
   alors BOVS=false (0), et BOVS=true (1) inversement. Dans le cas où
   A=B sur plusieurs niveaux consécutifs depuis le plus bas niveau de
   l'échantillon, le plugin cherche le 1er niveau où A est différent de
   B et retourne BOVS=false (0) si A < B à ce niveau, et BOVS=true (1)
   inversement.
-  Une variable booléenne BOEQ est également créée lors de l'utilisation
   de la clé --checkForEquality pour donner une indication de l'égalité
   de A par rapport à B au 1er niveau de l'échantillon. Plus
   précisémment, BOEQ=false (0) si A != B au premier niveau, et
   BOEQ=true (1) si A = B.
-  Par exemple, si on cherche les occurrences de l'évènement T=0 où T
   est la température de l'environnement (champ de référence) et 0 est
   l'isotherme 0 degC (champ de comparaison), le plugin indiquera
   BOVS=false (0) si T < 0 à la surface et true (1) , si T > 0. Autres
   exemples d'utilisation : recherche de couches nuageuses, de givrage,
   de couches chaudes et/ou froides, de zones d'énergie positive (CAPE).

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Hauteur géopotentielle GZ et/ou pression PX, selon le choix de
   l'utilisateur
-  Un champ de référence
-  Un champ ou une valeur de comparaison (selon la clé *comparisonType*)

\*Résultat(s):\*

-  Hauteur géopotentielle (dam) et/ou hauteur en pression (mb)
   associée(s) aux occurrences de l'événement A=B, par défaut AGZ et APX
   respectivement. Ce sont des champs où la dimension verticale
   correspond au nombre d'occurrences maximum demandées par
   l'utilisateur.
-  Variable booléenne, BOVS (2D)
-  Nombre d'occurrences de l'événement A=B, NBVS (2D)
   **Si** la clé checkForEquality est utilisée:
-  Variable booléenne, BOEQ (2D)

\*Algorithme:\*

-  `https://wiki.cmc.ec.gc.ca/images/2/28/Spooki_-_Algorithme_VerticalScan.odt <%20https://wiki.cmc.ec.gc.ca/images/2/28/Spooki_-_Algorithme_VerticalScan.odt>`__
-  https://wiki.cmc.ec.gc.ca/images/e/eb/Spooki_-_Algorithme_VerticalScan.pdf

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, recherche/search, balayage/scan, occurrence,
   niveau/level, vertical

\*Usage:\*

    Pour la clé --comparisonType:

    -  CONSTANTVALUE: compare chaque colonne du champ de référence à la
       même valeur constante
    -  VARIABLEVALUE: compare chaque colonne du champ de référence avec
       la valeur colocalisée horizontalement provenant du champ de
       comparaison 2D
    -  INTERSECTIONS: compare les colonnes colocalisées du champ 3D de
       référence et du champ 3D de comparaison pour trouver les
       intersections dans la verticale

    Pour la clé --comparisonValueOrField:

    -  Requiert une valeur pour : --comparisonType CONSTANTVALUE
    -  Requiert le nom d'un champ 2D avec la même couverture horizontale
       que le champ de référence pour: --comparisonType VARIABLEVALUE
    -  Requiert le nom d'un champ 3D colocalisé avec les champs de
       référence pour --comparisonType INTERSECTIONS

    | 
    | **Notes :**
    | Ce plugin peut être exécuté sous divers contextes :

    -  On peut chercher une constante sur toute la colonne (ex:
       recherche des niveaux de congélation où on cherche les
       occurrences TT = 0 deg C).
    -  On peut chercher une occurrence sur toute la colonne ou seulement
       sur un échantillon de la colonne.
    -  Le plugin peut recevoir en entrée un champ 3D ou seulement un
       profil

    \*Exemple d'appel:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VerticalScan/testsFiles/inputFile.std] >>
                    [VerticalScan --consecutiveEvents INF --referenceField TT --comparisonType CONSTANTVALUE --comparisonValueOrField 0 --outputVerticalRepresentation GEOPOTENTIAL --maxNbOccurrence 5 --epsilon 0.000001] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Contacts:**

    -  Auteur(e) : `Sandrine
       Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
    -  Codé par : `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__,
       Jonathan Cameron, `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
