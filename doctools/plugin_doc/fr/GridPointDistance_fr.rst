Français
--------

**Description:**

-  | Calcul des distances sur une grille horizontale entre chaque point
     dont on connaît la latitude et la longitude.
   | La distance peut être calculée de trois façons différentes sur
     chacun des axes de la grille:

   -  distance centrée           : en un point donné, distance angulaire
      entre le point précédent et le point suivant
   -  distance vers l'avant     : en un point donné, distance angulaire
      entre le point et le point suivant
   -  distance vers l'arrière    : en un point donné, distance angulaire
      entre le point et le point précédent

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Grille de points (sur au moins un axe) dont on connaît les latitudes
   et les longitudes respectives

\*Résultat(s):\*

-  Les distances GDX (axe des X) et GDY (axe des Y) entre chaque point
   de la grille donnée (mètres)

\*Algorithme:\*

    | Soit R, le rayon moyen de la Terre permettant de convertir les
      distances angulaires GDX et GDY de radians en mètres.
    | Pour tous les points i de latitude :math:`\lambda` (radians) et de
      longitude :math:`\varphi` (radians), on utilise selon
    | la valeur de la clé "differenceType", la formule trigonométrique
      appropriée pour calculer les distances angulaires:
    | Si axis = X alors
    |    Si différenceType = CENTERED alors
    |        
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i-1} \cdot
      \sin \lambda_{i+1} + \cos \varphi_{i-1} \cdot \cos \varphi_{i+1} \cdot
      \cos (\varphi_{i+1} - \varphi_{i-1})]$}`
    |          Pour le 1er niveau:
    |             
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i}
      \cdot \sin \lambda_{i+1} + \cos \varphi_{i} \cdot \cos \varphi_{i+1}
      \cdot \cos (\varphi_{i+1} - \varphi_{i})]$}`
    |          Pour le dernier niveau:
    |             
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i}
      \cdot \sin \lambda_{i-1} + \cos \varphi_{i} \cdot \cos \varphi_{i-1}
      \cdot \cos (\varphi_{i} - \varphi_{i-1})]$}`
    |    Sinon si différenceType = FORWARD alors
    |        
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i} \cdot
      \sin \lambda_{i+1} + \cos \varphi_{i} \cdot \cos \varphi_{i+1} \cdot
      \cos (\varphi_{i+1} - \varphi_{i})]$}`
    |          Pour le dernier niveau:
    |             
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i}
      \cdot \sin \lambda_{i-1} + \cos \varphi_{i} \cdot \cos \varphi_{i-1}
      \cdot \cos (\varphi_{i} - \varphi_{i-1})]$}`
    |    Sinon si différenceType = BACKWARD alors
    |        
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i} \cdot
      \sin \lambda_{i-1} + \cos \varphi_{i} \cdot \cos \varphi_{i-1} \cdot
      \cos (\varphi_{i} - \varphi_{i-1})]$}`
    |          Pour le 1er niveau:
    |             
      :math:`\mbox{ $GDX_{i} = R \cdot \arccos[\sin \lambda_{i}
      \cdot \sin \lambda_{i+1} + \cos \varphi_{i} \cdot \cos \varphi_{i+1}
      \cdot \cos (\varphi_{i+1} - \varphi_{i})]$}`
    |    Finsi
    | Sinon si axis = Y alors
    |    On procède de la même façon mais avec les points situés sur
      l'axe des Y
    | Finsi

| 
| ***Note:*** Les latitudes et longitudes doivent être en radians dans
  la formule trigonométrique. **Références:**

-  `Wikipedia: distance du grand
   cercle <http://fr.wikipedia.org/wiki/Distance_du_grand_cercle>`__

\*Mots clés:\*

-  GRILLE/GRID, point, distance, centrée/centered, arrière/backward,
   avant/forward

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd         --input $SPOOKI_DIR/pluginsRelatedStuff/GridPointDistance/testsFiles/inputFile.std] >>
                [GridPointDistance --axis X,Y --differenceType CENTERED] >>
                [WriterStd         --output /tmp/$USER/outputFile.std]"
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

 
