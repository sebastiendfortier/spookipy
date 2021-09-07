Français
--------

**Description:**

-  Calcul du cisaillement vertical du vent entre deux niveaux, en
   effectuant une différence centrée.

\*Méthode d'itération:\*

-  Colonne par colonne

| \*Dépendances:\*
| Deux niveaux verticaux:

-  UU, composante du vent selon l'axe des X.
-  VV, composante du vent selon l'axe des Y.
-  GZ, hauteur géopotentielle.

\*Résultat(s):\*

-  BS, cisaillement vertical du vent entre deux niveaux en 1/s
   Si on utilise l'option "--outputComponents YES":
-  BSU, composante du BS selon l'axe des X en 1/s.
-  BSV, composante du BS selon l'axe des Y en 1/s.

\*Algorithme:\*

    | Soit UU et VV, les composantes du vent en m/s.
    | Soit GZ, la hauteur géopotentielle en mètres.
    | Soit BS, le cisaillement vertical du vent entre 2 niveaux en 1/s.
    | Soit BSU et BSV, les composantes du cisaillement vertical du vent
      en 1/s.
    | Pour chaque niveau, K:

    | :math:` BS_{(K)}` =
      :math:`\mathrm{\sqrt{(BSU)_{(K)}^2 + (BSV)_{(K)}^2}}`
    | où
    | :math:`\mathrm{ BSU_{(K)}\; =\; \frac{[UU_{(K+1)} \, - \,
      UU_{(K-1)}]}{[GZ_{(K+1)} \, - \, GZ_{(K-1)}] }}`
    | et
    | :math:`\mathrm{ BSV_{(K)} \; =\; \frac{[VV_{(K+1)} \, - \,
      VV_{(K-1)}]}{[GZ_{(K+1)} \, - \, GZ_{(K-1)}] }}`

    | 
    | Note:

    -  Le calcul du cisaillement est fait avec une différence centrée.
       Exemple pour UU et N niveaux:
       Pour le 1er niveau:
       :math:`\mathrm{BSU_{(1)} \; =\; \frac{[UU_{(2)} \, - \,
        UU_{(1)}]}{[GZ_{(2)} \, - \, GZ_{(1)}] }}`
       Pour le dernier niveau:
       :math:`\mathrm{BSU_{(N)} \; =\; \frac{[UU_{(N)} \, - \,
        UU_{(N-1)}]}{[GZ_{(N)} \, - \, GZ_{(N-1)}] }}`

    \*Références:\*

    -  `Package de
       l'aviation <http://iweb/~afsypst/pluginsRelatedStuff/WindVerticalShear/reference/PackageAviation.pdf>`__

    \*Mots clés:\*

    -  MÉTÉO/WEATHER, cisaillement/shear, vent/wind, vertical,
       turbulence, aviation

    \*Usage:\*

    **Exemple d'appel:**

    .. code:: example

        ...
        spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/WindVerticalShear/testsFiles/inputFile.std] >>
                    [WindVerticalShear] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Contacts:**

    -  Auteur(e) : `Marc
       Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
    -  Codé par : `Luc
       Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__,
       `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
