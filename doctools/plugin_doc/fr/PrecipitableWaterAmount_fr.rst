Français
--------

**Description:**

-  Calcul de la quantité d'eau précipitable contenue dans une couche
   verticale déterminée. Consiste à sommer la vapeur d'eau entre la base
   et le sommet de cette couche.

\*Méthode d'itération:\*

-  Colonne par colonne

| \*Dépendances:\*
| Un des champs d'humidité (3D) suivants:

-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Température du point de rosée, TD
-  Écart du point de rosée, ES
-  Humidité relative, HR
   **et**
   Si la valeur de l'option "--base" ou "--top" est en unité de
   longueur:
-  Hauteur géopotentielle , GZ
   Si on utilise "--base SURFACE":
-  Pression de l'air à la surface, P0

\*Résultat(s):\*

-  Quantité d'eau précipitable, EP (champ 2D, mm)

\*Algorithme:\*

.. code:: example

    Soit HU(k) = humidité spécifique au niveau k en kg/kg
    Soit g     = accélération de la gravité (9.80616 m.s-2)
    Soit ρ     = masse volumique de l'eau (1000 kg.m-3)
    Soit EP    = eau précipitable en mm

.. code:: example

    Si la variable d'humidité en entrée n'est pas l'humidité spécifique, appeler le plugin HumiditySpecific avec les clés --iceWaterPhase BOTH --temperaturePhaseSwitch -40C

.. code:: example

    Calculer PX(k) la pression en hPa pour chaque niveau HU(k)

.. code:: example

    Zstart = valeur de la clé --base si en unité de longueur
    Pstart = niveau de pression où on commence à calculer EP
    Ztop   = valeur de la clé --top si en unité de longueur
    Pend   = niveau de pression où on arrête de calculer EP

.. code:: example

    Si la valeur de --base est en unité de pression
       Pstart = valeur donnée à la clé --base convertie en hPa
    Si la valeur de --base est en unité de longueur
       Pstart = valeur de --base convertie en pression en interpolant linéairement lnP entre deux niveaux
    Si la valeur de --base = SURFACE
       Pstart = P0

.. code:: example

    Si la valeur de --top est en unité de pression
       Pend = valeur donnée à la clé --top convertie en hPa
    Si la valeur de --top est en unité de longueur
       Pend = valeur de --top convertie en pression en interpolant linéairement lnP entre deux niveaux
    Si la valeur de --top = HIGHEST
       Pend = PX du niveau le plus haut (dans l'atmosphère) dans les données d'entrée

.. code:: example

    Pour convertir les valeurs en unité de longueur en pression:

.. code:: example

    Convertir PX pour chaque niveau de la colonne en ln(PX) puis envoyer à InterpolationVertical avec GZ.
    Appeler InterpolationVertical --outputGridDefinitionMethod USER_DEFINED
                                  --verticalLevel valeur de Pstart ou Pend
                                  --verticalLevelType METER_GROUND_LEVEL
                                  --interpolationType LINEAR
                                  --extrapolationType ABORT
                                  --outputField INTERPOLATED_FIELD_ONLY
    Convertir le résultat qui est en ln(PX) en valeur de pression.

.. code:: example

    Vérifier que Pstart > Pend
    EP=0

.. code:: example

    Do k=premier niveau à partir du sol, jusqu'au dernier niveau -1

.. code:: example

    Si PX(k) > Pstart et PX(K+1)> Pstart

.. code:: example

    Vérifier que EP=0.0
    K=K+1

.. code:: example

    Sinon si PX(k) = Pstart

.. code:: example

    Vérifier que EP=0.0

.. code:: example

    Si PX(K+1) > Pend
       EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
       K=K+1
    Sinon si PX(K+1) < Pend
       Interpoler HU en lnP pour trouver la valeur HUend à Pend
       EP = 1/(ρ*g) * 0.5 * (HUend + HU(K)) * ABS(Pend - PX(K))
       Sortir de la boucle
    Sinon si PX(K+1) = Pend
       EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
       Sortir de la boucle
    Fin si

.. code:: example

    Sinon si  PX(k) > Pstart et PX(K+1) < Pstart

.. code:: example

    Vérifier que EP=0.0
    Interpoler HU en lnP pour trouver la valeur HUstart à Pstart

.. code:: example

    Si PX(K+1) > Pend
       EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HUstart) * ABS(PX(k+1) - Pstart)
       K=K+1
    Sinon si PX(K+1) < Pend
       Interpoler HU en lnP pour trouver la valeur HUend à Pend
       EP = 1/(ρ*g) * 0.5 * (HUend + HUstart) * ABS(Pend - Pstart)
       Sortir de la boucle
    Sinon si  PX(K+1) = Pend
       EP = 1/(ρ*g) * 0.5 * (HU(k+1) + HUstart) * ABS(PX(k+1) - Pstart)
       Sortir de la boucle
    Fin si

.. code:: example

    Sinon si PX(k) < Pstart et PX(K+1) < Pstart

.. code:: example

    Si PX(K+1) > Pend
       EP = EP + 1/(p*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
       K=K+1
    Sinon si PX(K+1) < Pend
       Interpoler HU en lnP pour trouver la valeur HUend à Pend
       EP = EP + 1/(ρ*g) * 0.5 * (HUend + HU(K)) * ABS(Pend - PX(K))
       Sortir de la boucle
    Sinon si PX(K+1) = Pend
       EP = EP + 1/(ρ*g) * 0.5 * (HU(k+1) + HU(k)) * ABS(PX(k+1) - PX(k))
       Sortir de la boucle
    Fin si

.. code:: example

    Sinon
       Erreur !
    Fin si

.. code:: example

    Convertir EP en mm en multipliant par 10**5

.. code:: example

**Références:**

-  Tiré du programme opérationnel, eeaucol\ :sub:`fstd2000`.f

\*Mots clés:\*

-  MÉTÉO/WEATHER, eau/water, quantité/amount, précipitable/precipitable

\*Usage:\*

    **Notes :**
    L'utilisation de données en coordonnée verticale en pression n'est
    pas permise avec l'option "--base SURFACE" car ceci peut produire
    des résultats non fiables.

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitableWaterAmount/testsFiles/inputFile.std] >>
                [PrecipitableWaterAmount --base SURFACE --top HIGHEST] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Codé par : `Luc
   Pelletier <https://wiki.cmc.ec.gc.ca/wiki/User:Pelletierl>`__
   `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
   `Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

`Tests unitaires <PrecipitableWaterAmount_8cpp.html>`__

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
