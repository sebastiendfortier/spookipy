Français
--------

**Description :**

-  Calcul de la température, température du point de rosée, humidité
   relative, pression et hauteur d'une parcelle représentant la moyenne
   d'une couche.

\*Méthode d'itération :\*

-  Colonne par colonne

\*Dépendances :\*

-  Température de l'air recouvrant la couche désirée, TT (3D)
-  Hauteur géopotentielle recouvrant la couche désirée, GZ (3D)
-  Hauteur géopotentielle de la surface, GZ (2D) (ou GZG si GZ à la
   surface n'est pas disponible)

| \*et\* un des champs suivants recouvrant la couche désirée:

-  Humidité spécifique, HU (3D)
-  Humidité relative, HR (3D)
-  Rapport de mélange de la vapeur d'eau, QV (3D)
-  Température du point de rosée, TD (3D)
-  Écart du point de rosée, ES (3D)
   ***Note:*** : Assurez-vous de fournir à ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s) :\*

-  Température de la parcelle, MLTT (deg C)
-  Température du point de rosée de la parcelle, MLTD (deg C)
-  Pression de la parcelle, MLPX (hPa)
-  Humidité relative de la parcelle, MLHR (fraction)
-  Hauteur de la parcelle à partir du sol, MLZ (m)

\*Algorithme :\*

    | Appeler le plugin pour obtenir PX (hPa) dans la couche.
    | Appeler le plugin pour obtenir HU (kg/kg), si HU n'est pas
      disponible.
    | Appeler les fonctions d'interpolations linéaires (sur ln P et sans
      extrapolation permise) pour trouver les valeurs des champs se
      trouvant sur les niveaux de début et de fin de la couche désirée,
      si elles ne sont pas présentes dans les données entrées.
    | Calculer MLTT, MLPX et MLZ:

    #+begin\ :sub:`quote` TT - température (deg C)
    HU - humidité spécifique (kg/kg)
    TD - point de rosée (deg C)
    HR - humidité relative (fraction)
    GZ - hauteur géopotentielle (dam)
    Ki - niveau initial de la couche (obtenu par --base)
    Kt - niveau final de la couche (obtenu par --base et --delta)
    N - nombre de niveau entre Ki et Kt (obtenu à partir de données
    d'entrée)
    :math:` MLTT = \frac {\sum_{Ki}^{Kt} TT}{N+1}`
    :math:` MLPX = \frac {\sum_{Ki}^{Kt} PX}{N+1}`
    :math:` MLZ = ( \frac {\sum_{Ki}^{Kt} GZ}{N+1} - GZ(ground) ) *10.0 `

| Calculer MLTD et MLHR:

    | :math:` MLHU = \frac {\sum_{Ki}^{Kt} HU}{N+1} `
    | Appeler les plugins et pour obtenir TD et HR avec:
    |       TT = MLTT
    |       HU = MLHU
    |       PX = MLPX
    | Appeler le plugin pour renommer TD à MLTD et HR à MLHR.

#+end\ :sub:`quote`

**Références :**

-  Craven, J. P., R. E. Jewell, and H. E. Brooks, 2002: Comparison
   between observed convective cloud-base heights and lifting
   condensation level for two different lifted parcels. Wea.
   Forecasting, 17, 885-890.

\*Mots clés :\*

-  MÉTÉO/WEATHER, parcelle/parcel, couchemoyenne/meanlayer, convection,
   température/temperature, pression/pressure, humidité/humidity,
   pointderosée/dewpoint, hauteur/height

\*Usage:\*

    | 
    | **Notes :**
    | L'utilisation de données en coordonnée verticale en pression n'est
      pas permise avec l'option --base SURFACE car ceci peut produire
      des résultats non fiables.
    | Informations sur les metadonnées:

    -  Le verticalLevel (IP1 dans les fichiers RPN STD) indiquera la
       base de la couche moyenne.
    -  Les caractères 2 à 4 du pdsLabel (5 à 8 de l'etiket dans les
       fichiers RPN STD) indiqueront l'épaisseur de la couche moyenne.
       Le dernier de ces caractères indique l'unité (P pour hPa
       au-dessus de la base de la couche, Z pour mètres au-dessus de la
       base de la couche).

    \*Exemple d'appel:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ParcelMeanLayer/testsFiles/inputFile.std] >>
                    [ParcelMeanLayer --base SURFACE --delta 100mb --iceWaterPhase WATER] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Contacts:**

    -  Auteur(e) : Neil Taylor
    -  Codé par : `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
