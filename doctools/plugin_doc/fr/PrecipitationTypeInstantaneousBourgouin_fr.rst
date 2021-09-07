Français
--------

**Description:**

-  Calcul des types de précipitation instantanées à partir de la méthode
   de Bourgouin, basée sur l'énergie disponible dans les couches froides
   et chaudes en altitude. Plus précisément, cette méthode examine le
   profil de température et tient compte des énergies positives et
   négatives par rapport à l'isotherme 0 deg C pour décider du type de
   précipitation en fonction de valeurs énergétiques de référence.
   L'énergie positive (négative) est définie ici comme l'aire sur un
   téphigramme où la température est positive (négative,
   respectivement).
-  Les couches d'énergie, obtenues par la méthode de l'isotherme moyenne
   (plugin
   `EnergyMeanIsothermMethod <pluginEnergyMeanIsothermMethod.html>`__),
   sont délimitées par les niveaux de congélation (en pression) produits
   par le plugin `FreezingLevel <pluginFreezingLevel.html>`__.

\*Méthode d'itération:\*

-  Colonne par colonne

\*Dépendances:\*

-  Température de l'air, TT
-  Taux de précipitation total, RT
   ***Note:*** : Assurez-vous de fournir à  ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s) :\*

-  Type de précipitation, T6 (2D, sans unité). Valeur codée de 1 à 6
   telle que :
   1: pluie
   2: mélange pluie/neige
   3: verglas
   4: grésil
   5: neige
   6: taux de précipitation insuffisant (inférieur à 0.2mm/h)

\*Algorithme :\*

-  https://wiki.cmc.ec.gc.ca/images/f/f2/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.doc
-  https://wiki.cmc.ec.gc.ca/images/4/4b/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.pdf

\*Références :\*

-  Article de référence sur la methode de Bourgouin :
   https://wiki.cmc.ec.gc.ca/images/5/59/Spooki_-_Article_ref_Bourgouin.pdf
-  Inspiré du programme opérationnel ''gembrgouin''

\*Mots clés :\*

-  MÉTÉO/WEATHER, type, precipitation, instantanée/instantaneous,
   Bourgouin, congélation/freezing

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationTypeInstantaneousBourgouin/testsFiles/inputFile.std] >>
                ( [Copy] + [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 10 ]  ) >>
                [PrecipitationTypeInstantaneousBourgouin] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

|image0|

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 

.. |image0| image:: PrecipitationTypeInstantaneousBourgouin_graph.png

