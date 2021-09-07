Français
--------

**Description:**

-  Determiner les composantes UU et VV du vecteur vitesse du vent par
   rapport au vrai nord a partir de la direction meteorologique et du
   module du vecteur vitesse.

\*Méthode d'itération:\*

-  Calcul point par point.

\*Dépendances:\*

-  Module du vecteur vitesse du vent UV noeuds
-  Direction meteorologique du vent WD (deg).

\*Résultat(s):\*

-  UU et VV

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/d/d7/Spooki_-_Algorithme_Vecteur_to_composantes.pdf

\*Références:\*

-  tire de la sousroutine 'XY' du programme fortran helicte.f

\*Mots clés:\*

-  MÉTÉO/WEATHER, direction, vent/wind, météorologique/meteorological,
   composantes/components, module/modulus, vitesse/speed,
   azimutal/azimut

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindComponents/testsFiles/inputFile.std] >>
                [WindComponents] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
