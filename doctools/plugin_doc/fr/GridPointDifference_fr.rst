Français
--------

**Description:**

-  | Calcul des différences de valeurs d'un champ donné en chaque point
     de grille.
   | La différence peut être calculée de trois façons différentes sur
     chacun des axes de la grille:

   -  distance centrée           : en un point donné, différence de la
      valeur du champ entre le point précédent et le point suivant
   -  distance vers l'avant     : en un point donné, différence de la
      valeur du champ entre ce point et le point suivant
   -  distance vers l'arrière    : en un point donné, différence de la
      valeur du champ entre ce point et le point précédent

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ sur une grille ou sur au moins un des axes de calcul (X,Y,Z)

\*Résultat(s):\*

-  Différence(s) centrée(s), avant(s) ou arrière(s) d'un champ en chaque
   point de grille.

\*Algorithme:\*

.. code:: example

    Soit F un champ donné et N sa dimension selon un axe X donné (clé "axis")
    Soit n (n=1, N), le point à partir duquel on veut calculer la différence centrée, avant ou arrière du champ F.
    Le calcul selon l'axe X résulte en:

    Si différenceType = CENTERED alors
       F(1) = F(2) - F(1)
       F(n) = F(n+1) - F(n-1) pour 2 <= n <= N-1
       F(N) = F(N) - F(N-1)
    Sinon si différenceType = FORWARD alors
       F(N) = F(N) - F(N-1)
       F(n) = F(n+1) - F(n)  pour 1 <= n <= N-1
    Sinon si différenceType = BACKWARD alors
       F(1) = F(2) - F(1)
       F(n) = F(n) -F(n-1)   pour 2 <= n <= N
    Finsi

**Références:**

-  "Numerical Recipes: The Art of Scientific Computing" par W.H. Press,
   B.P. Flannery, S.A. Teukolsky et W.T. Vetterling

\*Mots clés:\*

-  GRILLE/GRID, point, difference, centrée/centered, arrière/backward,
   avant/forward

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/GridPointDifference/testsFiles/inputFile.std] >>
                [GridPointDifference --axis X,Y --differenceType CENTERED] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts**

-  Auteur(e) : `Marc
   Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
