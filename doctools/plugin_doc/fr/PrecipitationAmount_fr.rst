Français
--------

**Description:**

-  Calculer les accumulations de précipitations pour des intervalles
   temporels donnés.
-  Les divers intervalles sont définis par les clés paramétrables.

\*Méthode d'itération:\*

-  Différence temporelle, point par point

\*Dépendances:\*

-  Champs d'accumulation de précipitations à toutes les heures requises
   pour les calculs désirés.
-  Tous les types d'accumulation de précipitations qui se retrouvent
   dans o.dict peuvent être utilisés:
   Ex. PR, FR, PE, RN, SN, A[1-4], AE, AMX, ASG, ASH, ASN, FR[1\|2], PB,
   PC, PE[1\|2], PE2L, PM, PY, PZ, RN[1\|2], SN[1-3], SN10, SND, SNLR,
   etc

\*Résultat(s):\*

-  Champs (2D) d'accumulation de précipitations pour les intervalles
   temporels demandés, dans les mêmes unités que les dépendances.

\*Algorithme:\*

-  Appel du plugin
   `TimeIntervalDifference <pluginTimeIntervalDifference.html>`__ avec
   les valeurs des quatre clés paramétrables.
-  La clé --fieldName doit être utlisée seulement avec des champs
   choisis parmi la liste dans la section des Dépendances.

\*Références:\*

-  Inspiré du script opérationnel : "img.pcpn:sub:`intvl`"

\*Mots clés:\*

-  MÉTÉO/WEATHER, précipitations/precipitation, différence/difference,
   type, temps/time, intervalle/interval, accumulation

\*Usage:\*

    ***Note :*** Une seule valeur de chacune des listes des clés
    --interval et --step s'applique à une seul des intervalles temporels
    définis dans --rangeForecastHour. L'ordre des valeurs dans les
    listes des clés --interval et --step, doivent correspondre à l'ordre
    dans la liste de --rangeForecastHour.

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --ignoreExtended --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationAmount/testsFiles/inputFile.std] >>
                [PrecipitationAmount --fieldName SN --rangeForecastHour 0@48 --interval 3 --step 1] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:User:Klasam>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
