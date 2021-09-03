Français
--------

**Description:**

-  Calcul de la température équivalente associée à l'indice de
   refroidissement éolien au niveau du sol.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air (TT) à la surface
-  Composante UU du vent (selon l'axe des X sur la grille), à la surface
-  Composante VV du vent (selon l'axe des Y sur la grille), à la surface
   ***Note:*** : Assurez-vous de fournir à ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s):\*

-  Indice de refroidissement éolien, RE (deg C)

\*Algorithme:\*

    Soit TT(1), la température de l'air (deg C) à la surface (2 mètres)
    et UV(1), le module du vent (km.h-1) à la surface (10 mètres).
    L'indice de refroidissement, RE (sans unité), se calcule selon
    l'équation de Osczevski-Bluestein:
    si TT(1) <= 0 et UV(1) >= 5 alors :
        RE = :math:`\mathrm{13.1200 + 0.6215*TT(1) + (0.3965*TT(1) -
    11.3700)*UV(1)^{0.16}}`
    sinon
        RE = TT

**Références:**

-  [[http://journals.ametsoc.org/doi/abs/10.1175/BAMS-86-10-1453][The
   new wind chill equivalent temperature chart. Osczevski, R. and
   Bluestein, M., Amer. Meteor. Soc., 2005]]
-  `Wikipédia : indice de refroidissement
   éolien <http://fr.wikipedia.org/wiki/Refroidissement_%C3%A9olien>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, facteuréolien/windchill, facteur/factor,
   refroidissement/chill

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindChill/testsFiles/inputFile.std] >>
                [WindChill] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Besner <https://wiki.cmc.ec.gc.ca/wiki/User:Besnerm>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__, `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
