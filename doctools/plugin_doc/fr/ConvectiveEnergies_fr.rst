Français
--------

**Description:**

-  Calcul de l'énergie potentielle de convection disponible (CAPE),
   inhibition convective (CIN), et certaines variations de ceux-ci.
-  Le plugin est conçu de façon générique pour qu'il s'applique à
   n'importe quelle parcelle telle qu'une soulevée de la surface, une
   représentée par la moyenne d'une couche, la parcelle la plus instable
   et/ou toute(s) autre(s) parcelle(s) définie(s) par l'usager.
-  Par défaut, l'énergie est calculée sur toute la colonne jusqu'à 10
   hPa.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Température de l'air, TT
-  Hauteur géopotentielle, GZ
-  Hauteur géopotentielle de la surface, GZ (2D) ou GZG si GZ à la
   surface n'est pas disponible

| \*et\* un des champs suivants :

-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Température du point de rosée, TD
-  Écart du point de rosée, ES
-  Humidité relative, HR

\*Résultat(s):\*

-  **en** utilisant la correction pour la température virtuelle:

   -  VCP (J kg-1), somme de toutes les couches d'énergie positive de
      flottabilité dans une colonne, si on utilise "--liftedFrom
      SURFACE"
      ou DVCP (J kg-1) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MVCP (J kg-1) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UVCP (J kg-1) si on utilise "--liftedFrom
      MOST\ :sub:`UNSTABLE`"
   -  VCN (J kg-1), inhibition convective définie entre le niveau de
      soulèvement de la parcelle et le niveau de convection libre (NCL),
      si on utilise "--liftedFrom SURFACE"
      ou DVCN (J kg-1) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MVCN (J kg-1) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UVCN (J kg-1) si on utilise "--liftedFrom
      MOST\ :sub:`UNSTABLE`"

      -  **si** la clé outputLevelsConvection est utilisée:

         -  PVC(hPa), pression au niveau de convection libre optimal
            (NCL), si on utilise "--liftedFrom SURFACE"
            ou DPVC (hPa) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MPVC (hPa) si on utilise "--liftedFrom
            MEAN\ :sub:`LAYER`"
            ou UPVC (hPa) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  ZVC (m), hauteur au-dessus de la surface du niveau de
            convection libre optimal (NCL), si on utilise "--liftedFrom
            SURFACE"
            ou DZVC (m) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MZVC (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
            ou UZVC (m) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  PVE (hPa), pression au niveau d'équilibre optimal (NE), si
            on utilise "--liftedFrom SURFACE"
            ou DPVE (hPa) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MPVE (hPa) si on utilise "--liftedFrom
            MEAN\ :sub:`LAYER`"
            ou UPVE (hPa) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  ZVE (m), hauteur au-dessus de la surface du niveau
            d'équilibre optimal (NE), si on utilise "--liftedFrom
            SURFACE"
            ou DZVE (m) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MZVE (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
            ou UZVE (m) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"

-  **sans** utiliser la correction pour la température virtuelle:

   -  CAPE (J kg-1), somme de toutes les couches d'énergie positive de
      flottabilité dans une colonne, si on utilise "--liftedFrom
      SURFACE"
      ou DCP (J kg-1) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MCP (J kg-1) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UCP (J kg-1) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
   -  CINH (J kg-1), inhibition convective définie entre le niveau de
      soulèvement de la parcelle et le niveau de convection libre (NCL),
      si on utilise "--liftedFrom SURFACE"
      ou DCN (J kg-1) si on utilise "--liftedFrom USER\ :sub:`DEFINED`"
      ou MCN (J kg-1) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
      ou UCN (J kg-1) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"

      -  **si** la clé outputLevelsConvection est utilisée:

         -  PFC(hPa), pression au niveau de convection libre optimal
            (NCL), si on utilise "--liftedFrom SURFACE"
            ou DPFC (hPa) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MPFC (hPa) si on utilise "--liftedFrom
            MEAN\ :sub:`LAYER`"
            ou UPFC (hPa) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  ZFC (m), hauteur au-dessus de la surface du niveau de
            convection libre optimal (NCL), si on utilise "--liftedFrom
            SURFACE"
            ou DZFC (m) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MZFC (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
            ou UZFC (m) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  PEL (hPa), pression au niveau d'équilibre optimal (NE), si
            on utilise "--liftedFrom SURFACE"
            ou DPEL (hPa) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MPEL (hPa) si on utilise "--liftedFrom
            MEAN\ :sub:`LAYER`"
            ou UPEL (hPa) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"
         -  ZEL (m), hauteur au-dessus de la surface du niveau
            d'équilibre optimal (NE), si on utilise "--liftedFrom
            SURFACE"
            ou DZEL (m) si on utilise "--liftedFrom
            USER\ :sub:`DEFINED`"
            ou MZEL (m) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
            ou UZEL (m) si on utilise "--liftedFrom
            MOST\ :sub:`UNSTABLE`"

\*     Note :\* Les valeurs indéfinies associées au CAPE sont mises à -1
alors que les valeurs indéfinies associées au CINH sont mises à +1. Les
niveaux indéfinis associés avec LFC et EL sont mis à -300.

| **Algorithme:**

-  https://wiki.cmc.ec.gc.ca/images/a/a9/SPOOKI_-_Algorithme_ConvectiveEnergies.odt
-  https://wiki.cmc.ec.gc.ca/images/2/2d/SPOOKI_-_Algorithme_ConvectiveEnergies.pdf

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
   parcellesoulevée/liftedparcel, convection, CAPE, CIN

\*Usage:\*

    | ***Notes :***

    -  L'utilisation de données en coordonnée verticale en pression
       n'est pas permise avec l'option --base SURFACE car ceci peut
       produire des résultats non fiables.
    -  Pour les couches d'énergies non bornées:

       -  Le verticalLevel (IP1 dans les fichiers RPN STD) indiquera la
          surface, la base de la couche moyenne ou la base de recherche
          pour la couche la plus instable.
       -  Le userDefinedIndex (IP3 dans les fichiers RPN STD) indiquera
          la valeur de 10mb.

    -  Pour les couches d'énergies bornées:

       -  Le verticalLevel (IP1 dans les fichiers RPN STD) indiquera la
          valeur de la borne inférieure.
       -  Le userDefinedIndex (IP3 dans les fichiers RPN STD) indiquera
          la différence des hauteurs ou des températures OU (si encodé)
          la borne supérieure de la hauteur ou de la température.

    -  Pour les niveaux de convection libre et d'équilibre (lorsque la
       clé outputLevelsConvection est utilisée):

       -  Le userDefinedIndex (IP3 dans les fichiers RPN STD) indiquera
          la surface, la base de la couche moyenne ou la base de
          recherche pour la couche la plus instable.

    -  Lorsque les options --MeanLayer et --MostUnstable sont utilisées:

       -  Les caractères 2 à 4 du pdsLabel (5 à 8 de l'etiket dans les
          fichiers RPN STD) indiqueront l'épaisseur de la couche moyenne
          ou l'épaisseur de la couche la plus instable. Le dernier de
          ces caractères indique l'unité (P pour hPa au-dessus de la
          base de la couche, Z pour mètres au-dessus de la base de la
          couche).

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ConvectiveEnergies/testsFiles/inputFile.std] >>
                [ConvectiveEnergies --liftedFrom SURFACE --endLevel 10.0hPa --increment 10.0hPa --virtualTemperature NO] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : Neil Taylor
-  Codé par : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__ `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
