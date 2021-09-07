Français
--------

**Description:**

-  Calcul de l'indice de turbulence DVSI (Deformation Vertical Shear
   Index - développé par Ellrod)

\*Méthode d'itération:\*

-  Élément par élément

\*Dépendances:\* Trois niveaux verticaux:

-  Composante UU du vent (selon l'axe des X)
-  Composante VV du vent (selon l'axe des Y)

Deux niveaux verticaux (Inférieur et supérieur):

-  Hauteur géopotentielle GZ.

\*Résultat(s):\*

-  L'indice de turbulence (DVSI=Deformation Vertical Shear Index,
   variante de l'indice Ellrod) à chaque point de grille

\*Algorithme:\*

-  DVSI = DEF x VS x correction où correction = \|UV\|/45.0 (utilsant le
   niveau intermédiaire) (\|UV\| = module du vent calculé par ) DEF = la
   déformation du vent calculée par le plugin (utilsant le niveau
   intermédiaire) BS = le cisaillement vertical BS calculé par le plugin
   (utilsant les niveaux inférieur et supérieur) UV est en m/s, DEF est
   en (m/s)/100km et BS est en (m/s)/km

\*Références:\*

-  `Package de
   l'aviation <http://iweb.cmc.ec.gc.ca/cmc/bibliotheque/PREVISIONS/f_7.pdf>`__
   et l'article `Ellrod&Knapp
   (1992) <http://iweb/%7Eafsg003/doc/ClearAirTurbulence.pdf>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, turbulence, cisaillement/shear, vertical,
   déformation/deformation, vent/wind, aviation, dvsi, ellrod

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindTurbulenceDVSI/testsFiles/inputFile.std] >>
                [WindTurbulenceDVSI] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
