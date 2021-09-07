Français
--------

**Description:**

-  Calcul d'une différence temporelle de champs selon divers intervalles
   donnés.
-  Les divers intervalles sont définis par les clés paramétrables.
-  Ce plugin peut être utilisé, par exemple, pour le calcul des
   accumulations de précipitations.

\*Méthode d'itération:\*

-  Différence temporelle, point par point

\*Dépendances:\*

-  Les champs à toutes les heures requises pour les calculs désirés.

\*Résultat(s):\*

-  Différence temporelle de champs sur chaque intervalle, dans les mêmes
   unités que les dépendances.

\*Algorithme:\*

.. code:: example

    1) Créer une liste complète des paires de temps encadrant chaque intervalle désiré:

        Soit N le nombre d'intervalles temporels dans --rangeForecastHour
        Soit rangeStart(n) la première valeur du n ième intervalle temporel dans --rangeForecastHour
        Soit rangeEnd(n) la deuxième valeur du n ième intervalle temporel dans --rangeForecastHour
        Soit interval(n) la n ième valeur dans --interval
        Soit step(n) la n ième valeur dans --step
        Soit k le nombre total de calculs désirés

        k = 0
        Pour n = 1,N

           k = k + 1
           startime(k) = rangeStart(n)
           endtime(k) = 0.0

           Boucler aussi longtemps que ( startime(k) + interval(n) ) <= rangeEnd(n)
               endtime(k) = startime(k) + interval(n)
               Si endtime(k) < rangeEnd(n)
                  k = k + 1
                  startime(k) = startime(k-1) + step(n)
               fin si
           fin boucle

           n = n + 1
        fin

     2) Pour chaque champ dans --fieldName boucler sur chaque intervalles désirés:

        Soit M le nombre de champs dans --fieldName
        Soit VAR(m,x) le m ième champ dans --fieldName au temps x
        Soit RVAR(m,y) la valeur de la différence du champ VAR(m) entre deux temps
        Soit k le nombre de calculs désirés tel que calculé dans la partie 1.

        Pour m = 1,M
           ii = 0
           Pour ii < k+1
              RVAR(m,ii) = VAR(m,enditme(ii)) - VAR(m,startime(ii))
              ii = ii + 1
           fin
           m = m + 1
        fin

**Références:**

-  Inspiré du script opérationnel : "img.pcpn:sub:`intvl`"

\*Mots clés:\*

-  UTILITAIRE/UTILITY, différence/difference, accumulation, temps/time,
   temporel/temporal, intervalle/interval

\*Usage:\*

    ***Note:*** Une seule valeur de chacune des listes des clés
    --interval et --step s'appliquent à une seul des intervalles
    temporels définies dans --rangeForecastHour. L'ordre des valeurs
    dans les listes des clés --interval et --step, doivent correspondre
    à l'ordre dans la liste de --rangeForecastHour.

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --ignoreExtended --input $SPOOKI_DIR/pluginsRelatedStuff/TimeIntervalDifference/testsFiles/global20121217_fileSrc.std] >>
                [TimeIntervalDifference --fieldName PR --rangeForecastHour 0@177,0@60 --interval 12,3 --step 24,6] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
