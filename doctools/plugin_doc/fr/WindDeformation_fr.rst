Français
--------

**Description:**

-  Calcul de la déformation du vent horizontal

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Composante UU du vent (selon l'axe des X sur la grille).
-  Composante VV du vent (selon l'axe des Y sur la grille).

\*Résultat(s):\*

-  La déformation du vent, DEF (s-1)

\*Algorithme:\*

    La déformation du vent est une combinaison d'un facteur d'étirement
    ("stretching deformation") et d'un facteur de cisaillement
    ("shearing deformation"), ce qui se traduit par l'équation suivante
    où chacun de ces 2 facteurs est représenté respectivement :

    #+begin\ :sub:`quote` DEF =
    :math:`\sqrt{\left( \frac{\partial U}{\partial X} - \frac{\partial
      V}{\partial Y} \right)^2 + \left( \frac{\partial V}{\partial X} +
      \frac{\partial U}{\partial Y} \right)^2}`

Les dérivées partielles :math:`\frac{\partial}{\partial X} ` et :math:`
  \frac{\partial}{\partial Y}` des composantes horizontales du vent sont
calculées à l'aide des plugins
`GridPointDistance <pluginGridPointDistance.html>`__ et
`GridPointDifference <pluginGridPointDifference.html>`__ en utilisant
des différences centrées.

***Note:** L'unité* des composantes U et V doit être m.s-1

#+end\ :sub:`quote`

**Références:**

-  Voir la définition de la déformation dans l'article de `Ellrod&Knapp
   (1992) <http://iweb.cmc.ec.gc.ca/%7Eafsg003/doc/ClearAirTurbulence.pdf>`__
   ou dans le `Package de
   l'aviation <http://iweb.cmc.ec.gc.ca/cmc/bibliotheque/PREVISIONS/f_7.pdf>`__.

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, déformation/deformation, turbulence,
   aviation

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/testsFiles/inputFile.std] >>
                [WindDeformation] >>
                [WriterStd --output /tmp/$USER/outputFile.std  --noUnitConversion]"
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

 
