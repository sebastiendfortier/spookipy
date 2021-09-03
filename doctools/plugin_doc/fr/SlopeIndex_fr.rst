Français
--------

**Description:**

-  Cet indice de pente est en fait le produit scalaire du vecteur du
   vent (à 850, 700 ou 500 hPa) et du gradient topographique.
-  Plus l'indice est grand dans les valeurs négatives, plus on est en
   présence d'un effet de downslope, et inversement, plus l'indice est
   grand dans les valeurs positives, plus on est en présence d'un effet
   de upslope.
-  Cet indice est principalement utile lorsqu'on applique un traitement
   statistique spatial.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Composantes du vent à 850, 700 ou 500 hPa, UU et VV
   **et** un des champs suivants:
-  Élévation de la topographie, ME
-  Hauteur géopotentielle à la surface, GZ

\*Résultat(s):\*

-  Indice de pente, SLX (m/s)

\*Algorithme:\*

.. code:: example

    #Variables pertinentes
    SLX = Slope Index (m/s)
    float ME = Hauteur topographique (m)
    float UU = composante x du vent (KTS)
    float VV = composante y du vent (KTS)
    int fetch = nb de points de grille distant du point central i,j (default = 1)
    float dx = distance entre les 2 points selectionnes en x (m)
    float dy = distance entre les 2 points selectionnes en y (m)
    float A = 0.514444 = KTS -> m/s

    #Lecture de UU et VV a 850, 700 ou 500 (KTS)

    #Lecture de ME ou GZ surface (m)

    #Calcul du Slope Index (m/s)

    Pour chaque point de la grille, on calcul le produit scalaire du vecteur vent (à un certain niveau uniforme) et gradient topographique.
    Le gradient topographique est calculé de manière centrée, sauf pour les points à proximité des frontières d'une grille à aire limitée
    ou le gradient est calculé seulement dans le cadran de points disponibles. Si l'usager préfère exclure ces points, étant donné que le
    le calcul du gradient topographique ne peut pas etre centré, l'option --excludeEdges doit être utilisée et ces points de grille
    auront la valeur -999.

    Si (i+fetch) && (i-fetch) && (j+fetch) && (j-fetch) existent
    dx = distance entre le point (i+fetch,j) et (i-fetch,j)
    dy = distance entre le point (i,j+fetch) et (i,j-fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj-fetch)/dy]

    Sinon si l'option --excludeEdges, on retourne la valeur -999 

    Sinon Si (i-fetch) && (j-fetch) existent    
    dx = distance entre le point (i,j) et (i-fetch,j)
    dy = distance entre le point (i,j) et (i,j-fetch)
    SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

    Sinon Si (i+fetch) && (j+fetch) existent
    dx = distance entre le point (i,j) et (i+fetch,j)
    dy = distance entre le point (i,j) et (i,j+fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

    Sinon Si (i+fetch) && (j-fetch) existent
    dx = distance entre le point (i,j) et (i+fetch,j)
    dy = distance entre le point (i,j) et (i,j-fetch)
    SLXi,j = A*UUi*[(MEi+fetch-MEi)/dx] + A*VVj*[(MEj-MEj-fetch)/dy]

    Sinon
    dx = distance entre le point (i,j) et (i-fetch,j)
    dy = distance entre le point (i,j) et (i,j+fetch)
    SLXi,j = A*UUi*[(MEi-MEi-fetch)/dx] + A*VVj*[(MEj+fetch-MEj)/dy]

**Références:**

-  N/D

\*Mots clés:\*

-  MÉTÉO/WEATHER, slope/pente, upslope, downslope

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SlopeIndex/testsFiles/inputFile.std] >> 
                [SlopeIndex --fetch 2] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__
-  Codé par : `Guylaine Hardy, Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
