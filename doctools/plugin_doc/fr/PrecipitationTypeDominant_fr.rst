Français
--------

**Description:**

-  Trouve le type dominant de précipitations en choisissant le type avec
   le maximum d'accumulation. Deux champs sont créés pour chaque
   intervalle temporel défini par les données d'entrée. Pour un
   intervalle donné, le champ PDM indique le type et le sous-type
   dominant de précipitations et le champ QDM indique l'accumulation
   correspondante.

   ***Note:*** : Utiliser le plugin
   `PrecipitationAmount <pluginPrecipitationAmount.html>`__ si les
   données d'entrée ne définissent pas chaque intervalle désiré.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Obligatoires si la clé --microphysics a la valeur MY2 ou P3 ou
   BOURGOUIN:

   -  RN, accumulation de pluie
   -  SN, accumulation de neige
   -  FR, accumulation de pluie verglaçante
   -  PE, accumulation de grésil

-  Obligatoires si la clé --microphysics a la valeur MY2 ou P3:

   -  RN1, accumulation de bruine
   -  FR1, accumulation de bruine verglaçante
   -  SN1, accumulation de cristaux de glace
   -  SN3, accumulation de neige roulée

-  Obligatoires si la clé --microphysics a la valeur CUSTOM:

   -  Tous les champs spécifiés par les clés: --rain, --drizzle,
      --freezingRain, --freezingDrizzle, --snow, --graupel,
      --icePellets, --iceCrystal, --hail et --snowGrain.

\*Résultat(s):\*

-  PDM: Champ du type dominant et sous-type dominant de précipitations
   (sans unité, compris entre 100 et 500, champ 2D) sur chaque
   intervalle temporel.
-  QDM: Champ contenant l'accumulation correspondant au type dominant de
   précipitations (champ 2D en mètres).

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/b/b7/SPOOKI_-_Algorithme_PrecipitationTypeDominant.odt
-  https://wiki.cmc.ec.gc.ca/images/8/85/SPOOKI_-_Algorithme_PrecipitationTypeDominant.pdf

| \*/Notes sur les types:/\* :

-  Type: Le premier chiffre représente le type de précipitations.

   -  1\_\_: Liquide
   -  2\_\_: Verglaçant
   -  3\_\_: Grésil
   -  4\_\_: Solide
   -  5\_\_: Aucunes précipitations

-  Sous-type de précipitations: Les deux derniers chiffres sont selon le
   type de la table
   `table <http://www.nco.ncep.noaa.gov/pmb/docs/grib2/grib2_table4-201.shtml>`__.
   Les codes respectifs pour chaque sous-type sont donc:

   -  101: Pluie
   -  111: Bruine
   -  110: Grêle
   -  203: Pluie verglaçante
   -  212: Bruine verglaçante
   -  308: Grésil (ice pellets)
   -  409: Neige roulée (graupel; snow pellets)
   -  414: Grains de neige (snow grains)
   -  405: Neige
   -  413: Cristaux de glace

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  MÉTÉO/WEATHER, précipitations/precipitation, type, dominant,
   accumulation

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationTypeDominant/testsFiles/inputFile.std] >>
                [TimeIntervalDifference --fieldName RN,SN,FR,PE --rangeForecastHour 0@48,0@48 --interval 12,24 --step 12,24 --strictlyPositive] >>
                [PrecipitationTypeDominant --microphysics BOURGOUIN] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à  .

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
