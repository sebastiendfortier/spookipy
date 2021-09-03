Français
--------

**Description:**

-  Calcul du tourbillon absolu.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Composante du vent selon l'axe des X sur la grille, UU
-  Composante du vent selon l'axe des Y sur la grille, VV

\*Résultat(s):\*

-  Tourbillon absolu, QQ (1/s)

\*Algorithme:\*

    | Appeler le plugin pour obtenir le paramètre de Coriolis, CORP
      (1/s).
    | Soit UU (m/s) et VV (m/s), respectivement les composantes du vent
      selon les axes des X et des Y.
    | Soit :math:`\varphi` (radians), la latitude.
    | Faire une dérivée décentrée sur une grille régionale pour les
      bordures.
    | Calculer le tourbillon absolu, QQ (1/s), avec la formule suivante:
    | :math:`\mathrm{QQ_{i,j} = ( VV_{i+1,j} - VV_{i-1,j} ) / ( X_{i+1,j} -
      X_{i-1,j} ) - ( UU_{i,j+1} * cos\varphi_{i,j+1} - UU_{i,j-1} *
      cos\varphi_{i,j-1} ) / ( ( Y_{i,j+1} - Y_{i,j-1} ) * cos\varphi_{i,j}
      ) + CORP_{i,j}}`

**Références:**

-  "An Introduction to Dynamic Meteorology", Holton, James R.

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, tourbillon/vorticity, absolute/absolu,
   Coriolis

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VorticityAbsolute/testsFiles/inputFile.std] >>
                [VorticityAbsolute] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Codé par : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
