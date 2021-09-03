Français
--------

**Description:**

-  Il s'agit d'un calcul de moyenne spatiale 2-D pondérée selon un type
   de noyau.
-  Le noyau peut prendre la forme de différentes fonctions, notamment
   une Gaussienne.
-  Dans le cas où ce calcul est appliqué à un champ binaire (0,1), on
   peut interpréter le résultat comme une densité de probabilité (PDF).

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un ou plusieur champ(s) sur une grille
-  Champ ME (un seul pas de temps donné) si option altDiffMax est
   utilisée
-  Champ MG (un seul pas de temps donné) si option landFracDiffMax est
   utilisée
-  Champ SLX (les mêmes temps de prévision du champ X) si option
   slopeIndexDiffMax est utilisée

\*Résultat(s):\*

-  Une moyenne pondérée selon le type de noyau.

\*Algorithme:\*

.. code:: example

    Pour chaque point de la grille, on calcul la moyenne à partir d'un ensemble de points grille définie par un rayon de
    recherche. Cette moyenne peut être pondérée selon une Gaussienne ou être uniforme. Dans le cas d'une grille à aire limitée, 
    le calcul de la moyenne aux points de grille à proximité des frontières est calculé avec un échantillon de points plus 
    restraint qu'ailleurs sur la grille. Si l'usager préfère exclure ces points, étant donné que le rayon de recherche ne peut 
    être totalement respecté, l'option --excludeEdges doit être utilisée et ces points de grille auront la valeur -999.
    Cet algorithme permet également de restreindre notre échantillon de points à certaines conditions spécifiques comme la 
    topographie, la proportion terre-eau, un indice de pente et une certaine plage de valeurs.

    ----------
    -Définition des variables importantes-
    ----------
    Rayon de recherche = r
    Distance entre un point de grille quelconque et le point de grille central traité = d
    Paramètre de lissage = h
    distanceType = POINTS ou KM
    Sommation des poids = Smax
    Sommation des valeurs pondérées= Sum
    La moyenne = Moy
    altDiffMax = Seuil maximum de différence d'altitude (ME) en valeur absolue acceptable entre le point de grille traité et ceux servant à calculer la moyenne
    landFracDiffMax = Seuil maximum de différence de la fraction de terre (MG) en valeur absolue acceptable entre le point de grille traité et ceux servant à calculer la moyenne
    slopeIndexDiffMax = Seuil maximum de différence de l'indice de pente (SLX) en valeur absolue acceptable entre le point de grille traité et ceux servant à calculer la moyenne
    minValue = Valeur min pour inclure un point dans le calcul de la moyenne (ex: si minValue = 3, la moyenne sera calculé seulement avec les points > 3)
    maxValue = Valeur max pour inclure un point dans le calcul de la moyenne (ex: si maxValue = 10, la moyenne sera calculé seulement avec les points < 10)
    diff_me_abs = |ME(i,j) - ME(i+a,j+b)]|
    diff_mg_abs = |MG(i,j) - MG(i+a,j+b)]|
    diff_slx_abs = |SLX(i,j) - SLX(i+a,j+b)]|

    ----- 
    -Définition des 2 types de kernel-
    ------
    Si --kernelType GAUSSIAN
    kernel(d,h) = exp((-0.5*(d^2))/h^2)

    Si --kernelType UNIFORM
    kernel(d,h) = 1

    Calcul de la moyenne pour tous les points de grille, si possible 

    Si distanceType = POINTS, la distance d entre le point de grille central et ceux autour est calculée avec l'équation de  
    Pythagore et si distanceType = KM, on utilise le plugin GridPointDistance

    On boucle sur tous les points de grille

    Si l'option --excludeEdges est utilisée, 
    On s'assure que la distance entre ce point et la frontière de la grille soit >= r
    Sinon ce point = -999

    Smax=0

    Si d <= r &&  diff_me_abs <= altDiffMax && diff_mg_abs <= landFracDiffMax && diff_slx_abs <= slopeIndexDiffMax && valeur(X) > minValue & valeur(X) < maxValue 

    On calcule la valeur maximale de la sommation pour les points à l'intérieur du rayon de recherche, avec une différence d'altitude (ME) en valeur absolue <= altDiffMax, 
    avec une différence de fraction de la terre (MG) en valeur absolue <= landFracDiffMax, avec une différence d'indice de pente (SLX) en valeur absolue <= slopeIndexDiffMax, avec une valeur > minValue
    et finalement avec une valeur < maxValue


    Seul le rayon de recherche est obligatoire

    Donc, pour ces points de grille respectant ces conditions, on calcul

    Smax = Smax + kernel(d,h,kernelType)
    Sum = Sum + kernel(d,h,kernelType)*valeur(du point de grille)


    Une fois tous les points à l'intérieur du rayon de recherche comptabilisés, la moyenne est normalisée :
    Moy = Sum/Smax

**Références:**

-  `Estimation par densite de
   noyau <https://en.wikipedia.org/wiki/Kernel_density_estimation>`__
-  `Fonction
   Gaussienne <https://en.wikipedia.org/wiki/Gaussian_function>`__
-  `Previsions
   orages <https://wiki.cmc.ec.gc.ca/wiki/File:Forecasting_thunderstorms.pptx>`__
-  `HRDPS <https://wiki.cmc.ec.gc.ca/wiki/File:HRDPS_EarlyResults2015_v2.pptx>`__

\*Mots clés:\*

-  UTILITAIRE/UTILITY, statistique/statistics, noyau/kernel, estimation,
   probabilité/probability, gaussienne/gaussian, pdf, lissage/smoothing,
   normal, distribution

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SpatialWeightedAveraging/testsFiles/inputFile.std] >>
                [SpatialWeightedAveraging --searchRadius 15 --kernelType GAUSSIAN --distanceType KM --smoothingParameter 5] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteurs : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__, / `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__
-  Codé par : `Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/Louise_Faust>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
