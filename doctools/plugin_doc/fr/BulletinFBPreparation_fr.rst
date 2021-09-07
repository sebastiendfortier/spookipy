Français
--------

**Description:**

-  Préparation des données de vent et température, interpolées sur un
   ensemble de stations canadiennes et aux hauteurs 3000, 6000, 9000,
   12000 et 18000 pieds, en vue d'écrire des bulletins FBCN CWAO à 06,
   12 et 24h, et/ou de produire des images pour l'aviation.

\*Méthode d'itération :\*

-  Ne s'applique pas

\*Dépendances:\*

-  Composante UU du vent (selon l'axe des X)
-  Composante VV du vent (selon l'axe des Y)
-  Température de l'air, TT
-  Altitude géopotentielle, GZ
   ***Note:*** Le module du vent (UV) et la direction du vent
   météorologique (WD) ne peuvent être fournis en dépendances à ce
   plugin (voir algorithme).

\*Résultat(s):\*

-  Module du vent UV (noeuds) calculé aux stations et aux hauteurs 3000,
   6000, 9000, 12000 et 18000 pieds
-  Direction du vent météorologique WD (deg) calculée aux stations et
   aux hauteurs 3000, 6000, 9000, 12000 et 18000 pieds
-  Température de l'air TT (deg C), interpolée aux stations et aux
   hauteurs 3000, 6000, 9000, 12000 et 18000 pieds
-  Altitude géopotentielle GZ (dam) à la surface, interpolée aux
   stations
-  Champ TerrainElevation (pieds) regroupant les élévations terrestres
   de chacune des stations
-  Champ StationAlphaID (4 lettres maximum) regroupant les codes
   d'identification de chacune des stations
-  Champ FictiveStationFlag booléen indiquant le statut réel ou fictif
   de chacune des stations

\*Algorithme:\*

-  Interrogation de la base de données de stations pour extraire à
   chacune des stations utilisées pour les bulletins FB :
     - Les latitudes des stations (degrés décimaux signés)
     - Les longitudes des stations (degrés décimaux signés)
-  Interpolation horizontale bi-cubique aux stations sélectionnées des
   champs UU, VV, TT et GZ
-  Interpolation verticale linéaire des champs UU, VV, et TT aux
   hauteurs 3000, 6000, 9000, 12000 et 18000 pieds, converties en
   mètres, pour l'interpolation en hauteur géométrique
-  Calcul de UV et WD, à partir de UU et VV en chaque point (lat,lon)
   associé à chaque station, défini sur une grille de référence de type
   "nuage de points" (correspondant à une grille de type L dans le cas
   particulier des fichiers standards)
-  Interrogation de la base de données pour obtenir les champs
   supplémentaires suivants, nécessaires à l'écriture des bulletins :
     - L'élevation terrestre de chaque station (mètres)
     - Le code d'identification de chaque station (4 lettres maximum)
     - Un champ booléen indiquant pour chacune des stations s'il s'agit
   ou non d'une station fictive

\*Mots clés:\*

-  PRODUIT/PRODUCT, aviation, bulletin, vent/wind,
   température/temperature, FBCN, station, interpolation,
   préparation/preparation, verticale/vertical

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/BulletinFBPreparation/testsFiles/inputFile.std] >>
                [BulletinFBPreparation] >>
                [WriterAsciiBulletinFB --outputPath /tmp/]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
