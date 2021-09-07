Français
--------

**Description:**

-  Calcul du contenu en eau liquide surfondue.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air, TT (C)

-  Densité de l'air, M3 (kg/m3)

   **et** si la clé paramétrable --origin est TOTAL ou ALL, les champs
   suivants sont requis:

-  Rapport de melange masse du nuage, MPQC (kg/kg)

-  Rapport de melange masse de pluie, MPQR (kg/kg)

   **et** si la clé paramétrable --origin est RAIN ou CLOUD, le champs
   approprié selon la clé parmis les mêmes choix est requis.

\*Résultat(s):\*

-  Contenu en eau liquide surfondue, SLW (kg/m3)
-  Contenu en eau liquide surfondue dans les nuages uniquement, SLWC
   (kg/m3)
-  Contenu en eau liquide surfondue dans la pluie et/ou la bruine
   uniquement, SLWR (kg/m3)

\*Algorithme:\*

.. code:: example

    Si la valeur de la clé --origin est TOTAL:
        Si TT < 0
            SLW = M3 * ( MPQC + MPQR )
        Sinon:
            SLW = 0

    Si la valeur de la clé --origin est RAIN:
        Si TT < 0
            SLWR = M3 * ( MPQR )
        Sinon:
            SLWR = 0

    Si la valeur de la clé --origin est CLOUD:
        Si TT < 0
            SLWC = M3 * ( MPQC )
        Sinon:
            SLWC = 0

    Si la valeur de la clé --origin est ALL:
        Calculer les variables SLW, SLWC et SLWR en utilisant les formules ci-dessus.

**Références:**

`Calcul de la densité de
l'air <https://wiki.cmc.ec.gc.ca/wiki/Wind_energy_and_icing_forecasting_version3#Computing_SLW_.28supercooled_liquid_water_content_.7C_Densit.C3.A9_des_gouttelettes_d.27eau_liquide_en_surfusion.29,>`__

**Mots clés:**

-  MÉTÉO/WEATHER, eau liquide surfondue/supercooled liquid water

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SupercooledLiquidWaterContent/testsFiles/inputFile.std] >>
                [SupercooledLiquidWaterContent --origin TOTAL] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Agnes
   Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Codé par : `Antoine
   Boisvert <https://wiki.cmc.ec.gc.ca/wiki/User:Boisvertan>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à  .

`Tests unitaires <SupercooledLiquidWaterContentTests_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
