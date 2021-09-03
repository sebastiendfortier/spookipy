Français
--------

Description:
~~~~~~~~~~~~

Calcul de la direction meteorologique (provenance du vecteur par rapport
au nord) à partir de ses 2 composantes horizontales.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Composante UU du vent (selon l'axe des X sur la grille). Composante VV
du vent (selon l'axe des Y sur la grille).

Résultat(s):
~~~~~~~~~~~~

Direction météorologique du vent, WD, en degrees.

Algorithme:
~~~~~~~~~~~

    Soit WD, la direction: Si on calcule la direction selon le
    référentiel météorologique (--orientationType WIND), alors : la
    fonction gduvfwd de la librairie EZSCINT est utilisée pour calculer
    la direction d'où vient le vecteur par rapport au nord

Références:
~~~~~~~~~~~

Ne s'applique pas

Mots clés:
~~~~~~~~~~

MÉTÉO/WEATHER, direction/direction, vent/wind, vitesse/speed

Usage:
~~~~~~

#. Exemple d'appel:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std").to_pandas()
       s=spooki.WindDirection(records).compute()
       fstpy.StandardFileWriter("/tmp/"+$USER+"/outputFile.std",records).to_fst()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) : `Maryse
Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__

Codé par : `François
Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

Calculation of the meteorological wind direction (where the vector is
coming from with respect to north) from its 2 horizontal components.

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

UU component of the wind (along the X axis of the grid). VV component of
the wind (along the Y axis of the grid).

Result(s):
~~~~~~~~~~

Meteorological wind direction, WD, in degrees.

Algorithm:
~~~~~~~~~~

    For WD, the direction : If the direction is calculated with the
    meteorological convention (--orientationType WIND), then : the
    gduvfwd function of the EZSCINT library is used to calculate the
    direction of where the vector is coming from with respect to north

Reference:
~~~~~~~~~~

Does not apply

Keywords:
~~~~~~~~~

MÉTÉO/WEATHER, direction/direction, vent/wind, vitesse/speed

Usage:
~~~~~~

#. Call example:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/WindModulusAndDirection/testsFiles/inputFile.std").to_pandas()
       s=spooki.WindDirection(records).compute()
       fstpy.StandardFileWriter("/tmp/"+$USER+"/outputFile.std",records).to_fst()

Contacts:
~~~~~~~~~

Author : `Maryse
Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__

Coded by : `François
Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
