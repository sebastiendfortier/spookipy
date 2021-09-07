Français
--------

**Description:**

-  Calcul du champ de pression pour une coordonnée verticale donnée.
-  La définition des différentes coordonnées est disponible dans `ce
   document. <https://wiki.cmc.ec.gc.ca/images/0/01/Spooki_-_Definitions_coordvert.pdf>`__
-  Possibilité de calculer la pression dans le cas d'une `atmosphère
   normalisée <http://fr.wikipedia.org/wiki/Atmosph%C3%A8re_normalis%C3%A9eatmosphère%20normalisée>`__
   (pression constante).
-  D'autres types de coordonnées verticales pourront être ajoutées et
   documentées dans le futur.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ quelconque sur un ensemble de niveaux verticaux donnés

\*Résultat(s):\*

-  Champ de pression PX (hPa, ou mb), sur l'ensemble des niveaux donnés

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/5/5c/Spooki_-_Algorithme_du_plugin_Pressure.pdf

\*Références:\*

-  Inspiré de l'utilitaire r.hy2pres de la librairie RMNLIB de RPN

\*Mots clés:\*

-  MÉTÉO/WEATHER, pression/pressure, niveau/level,
   coordonnée/coordinate, r.hy2pres

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Pressure/testsFiles/inputFile.std] >>
                [Pressure --coordinateType ETA_COORDINATE --referenceField TT] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à .

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
