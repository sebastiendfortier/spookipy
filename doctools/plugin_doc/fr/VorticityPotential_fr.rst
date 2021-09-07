Français
--------

**Description:**

-  Calcul du tourbillon potentiel d'Ertel (Ertel's potential vorticity)
   ou plus simplement PV.

\*Méthode d'itération:\*

-  Colonne par colonne.

\*Dépendances:\*

-  Composante du vent selon l'axe des X sur la grille, UU

-  Composante du vent selon l'axe des Y sur la grille, VV

-  Température de l'air, TT

   | ***Note:*** : Assurez-vous de fournir à ce plugin les dépendances
     ci-haut mentionnées ou alors, les résultats des
   | plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
     Pour plus de détails sur cet usage
   | alternatif, voir la page de
     `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s):\*

-  Tourbillon potentiel, PV (en unité PVU), 1 PVU = 1.e-6 K m\ :sup:`2`
   / ( kg s).

\*Algorithme:\*

.. code:: example

    Soit UU (m/s) et VV (m/s), respectivement les composantes du vent selon les axes des X et des Y.
    Soit QQ (1/s),   le tourbillon absolu.
    Soit PX (hPa),   la pression du modèle.
    Soit TT (K),     la température de l'air.
    Soit TH (K),     la température potentielle.
    Soit CORP (1/s), le paramètre de coriolis.

    Calculer le tourbillon potentiel d'Ertel, PV (en unité PVU):

    grav     = 9.806160000000 (accélération de gravité m s-2)
    ThetaMax = 380K

    Boucle k sur les niveaux :
        Boucle sur j :
            Boucle sur i :
                Si theta du point courant est plus grand que ThetaMax :
                    Mettre le PV à la valeur de la clé --PVU, mais du même signe que le paramètre de Coriolis
                Sinon 
                    Calculer PV (voir ci-bas)
                    Convertir le résultat en PVU 
                Fin si
            Fin de boucle sur i
        Fin de boucle sur j
    Fin de boucle sur k

    Calcul de PV:
    La dérivée partielle du log de theta selon PX ne doit pas être zero,
    car on divise par cette quantité.
    On la limite à -1.e-7 (cette quantité est négative)
    :math:`\mathrm{ DPX = ( ( PX_{i,j,k+1} - PX_{i,j,k-1} ) * 100. )}`
    :math:`\mathrm{ DTH = ( TH_{i,j,k+1} - TH_{i,j,k-1} )}`
    :math:`\mathrm{ PV_{i,j,k} = -grav * ( QQ_{i,j} - 1. / ( TT_{i,j} * min(
    -1.e-7, log( TH_{i,j,k+1} / TH_{i,j,k-1} ) / DPX ) ) * }`
              
    :math:`\mathrm{ ( ( VV_{i,j,k+1} - VV_{i,jk-1} ) / DPX * (
    TT_{i+1,j} - TT_{i-1,j} ) / ( X_{i+1,j} - X_{i-1,j} ) - (
    UU_{i,j,k+1} - UU_{i,j,k-1} ) / DPX * }`
              
    :math:`\mathrm{ ( TT_{i,j+1} - TT_{i,j-1} ) / ( Y_{i,j+1} -
    Y_{i,j-1} ) ) ) * DTH / DPX }`

**Références:**

-  Bluestein, H. B, 1992. Synoptic-Dynamic Meteorology in Midlatitudes,
   Volume I.
-  Code Fortran d'André Plante pressure\ :sub:`onpvsurface`.F90 et
   mod\ :sub:`pv`.F90, git clone
   `git@g.nosp@m.itla.nosp@m.b.sci.nosp@m.ence.nosp@m..gc.c.nosp@m.a <#>`__:cmdn:sub:`utils`/utilitaires.git

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, tourbillon/vorticity, potentiel/potential

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VorticityPotential/testsFiles/inputFile.std] >>
                [VorticityPotential --maxPVU 2.0] >>
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

 
