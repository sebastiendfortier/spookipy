Français
--------

**Description:**

-  Calcul des(s) niveau(x) de convection libre (NCL) et/ou d'équilibre
   (NE), basé sur la comparaison entre la température virtuelle d'une
   parcelle et celle de son environnement. Un calcul n'utilisant pas la
   correction de la température virtuelle est aussi disponible. Le
   plugin permet d'appliquer un NCL à  partir du sol pour le cas d'une
   couche super-adiabatique, ainsi que plusieurs NCL et/ou NE
   correspondants à  plusieurs couches instables (température de la
   parcelle plus chaude que celle de environnement).
-  Ce plugin est conçu de façon générique pour qu'il s'applique à 
   n'importe quelle situation telle qu'une parcelle soulevée à  partir
   de la surface, une parcelle représentant une couche moyenne, une
   parcelle représentant la couche plus instable et/ou toute(s) autre(s)
   situation de parcelle(s) définie(s) par l'usager.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Température de l'air de l'environnement, TT (3D)
-  Hauteur géopotentielle de l'environnement, GZ (3D)
-  Hauteur géopotentielle de la surface, GZ (2D) ou GZG si GZ à  la
   surface n'est pas disponible

| \*et\* un des champs suivants de l'environnement:

-  Humidité spécifique, HU (3D)
-  Rapport de mélange de la vapeur d'eau, QV (3D)
-  Température du point de rosée, TD (3D)
-  Écart du point de rosée, ES (3D)
-  Humidité relative, HR (3D)

\*Résultat(s):\*

-  **en** utilisant la correction pour la température virtuelle:

   -  NVC (2D), nombre de niveaux de convection libre, si on utilise
      "--liftedFrom SURFACE"
      ou DNVC (2D) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MNVC (2D) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UNVC (2D) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  PVC(hPa), pression au NCL, si on utilise "--liftedFrom SURFACE"
      ou DPVC (hPa) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MPVC (hPa) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UPVC (hPa) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  ZVC (m), hauteur au-dessus de la surface du NCL, si on utilise
      "--liftedFrom SURFACE"
      ou DZVC (m) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MZVC (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UZVC (m) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  NVE (2D), nombre de niveaux d'équilibre, si on utilise
      "--liftedFrom SURFACE"
      ou DNVE (2D) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MNVE (2D) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UNVE (2D) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  PVE (hPa), pression au NE, si on utilise "--liftedFrom SURFACE"
      ou DPVE (hPa) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MPVE (hPa) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UPVE (hPa) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  ZVE (m), hauteur au-dessus de la surface du NE, si on utilise
      "--liftedFrom SURFACE"
      ou DZVE (m) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MZVE (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UZVE (m) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"

-  **sans** utiliser la correction pour la température virtuelle:

   -  NLFC (2D), nombre de niveaux de convection libre, si on utilise
      "--liftedFrom SURFACE"
      ou DNFC (2D) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MNFC (2D) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UNFC (2D) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  PFC(hPa), pression au NCL, si on utilise "--liftedFrom SURFACE"
      ou DPFC (hPa) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MPFC (hPa) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UPFC (hPa) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  ZFC (m), hauteur au-dessus de la surface du NCL, si on utilise
      "--liftedFrom SURFACE"
      ou DZFC (m) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MZFC (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UZFC (m) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  NEL (2D), nombre de niveaux d'équilibre, si on utilise
      "--liftedFrom SURFACE"
      ou DNEL (2D) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MNEL (2D) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UNEL (2D) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  PEL (hPa), pression au NE, si on utilise "--liftedFrom SURFACE"
      ou DPEL (hPa) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MPEL (hPa) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UPEL (hPa) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  ZEL (m), hauteur au-dessus de la surface du NE, si on utilise
      "--liftedFrom SURFACE"
      ou DZEL (m) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MZEL (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UZEL (m) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"

\*     Note :\* Les niveaux indéfinis associés avec LFC et EL sont mis à
-300.

| **Algorithme:**

-  https://wiki.cmc.ec.gc.ca/images/3/3b/SPOOKI_-_Algorithme_LevelOfFreeConvectionAndEquilibrium.odt
-  https://wiki.cmc.ec.gc.ca/images/3/37/SPOOKI_-_Algorithme_LevelOfFreeConvectionAndEquilibrium.pdf

\*Références:\*

-  Doswell, C. A. and E. N. Rasmussen, 1994: The effect of neglecting
   the virtual temperature correction on CAPE calculations. Wea.
   Forecasting, 9, 625-629.
-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology in
   Midlatitudes. Wiley-Blackwell, 407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature,
   parcellesoulevée/liftedparcel, pression/pressure, convection,
   niveau/level

\*Usage:\*

    | 
    | ***Notes :***
    | L'utilisation de données en coordonnée verticale en pression n'est
      pas permise avec l'option --base SURFACE car ceci peut produire
      des résultats non fiables.
    | Lorsque les options --MeanLayer et --MostUnstable sont utilisées:

    -  Le userDefinedIndex (IP3 dans les fichiers RPN STD) indiquera la
       base de la couche moyenne ou la couche la plus instable.
    -  Les caractères 2 à 4 du pdsLabel (5 à 8 de l'etiket dans les
       fichiers RPN STD) indiqueront l'épaisseur de la couche moyenne ou
       l'épaisseur de recherche pour la couche la plus instable. Le
       dernier de ces caractères indique l'unité (P pour hPa au dessus
       de la base de la couche, Z pour mètres au dessus de la base de la
       couche).

    \*Exemple d'appel:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/LevelOfFreeConvectionAndEquilibrium/testsFiles/inputFile.std] >>
                    [LevelOfFreeConvectionAndEquilibrium --liftedFrom SURFACE --endLevel 100.0hPa --increment 10.0hPa --virtualTemperature NO --outputField LFC_PRESSURE,LFC_HEIGHT,EL_PRESSURE,EL_HEIGHT --outputLevels MULTIPLE_VALUES] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Contacts:**

    -  Auteur(e) : Neil Taylor : `Khanh-Hung
       Lam <https://wiki.cmc.ec.gc.ca/wiki/User:Lamk>`__
    -  Codé par : `Jonathan
       St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__ `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
