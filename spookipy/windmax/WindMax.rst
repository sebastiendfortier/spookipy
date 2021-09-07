Français
--------

**Description:**

-  Calcul de la valeur maximale du module du vent déterminée selon la
   verticale, ainsi que les composantes horizontales du vent et le
   niveau de pression correspondant.

\*Méthode d'itération:\*

-  colonne par colonne

\*Dépendances:\*

-  Composante UU du vent (selon l'axe des X sur la grille)
-  Composante VV du vent (selon l'axe des X sur la grille)
-  Champ de pression PX

\*Résultat(s):\*

-  Module du vent maximal, UV ( noeuds)
-  Composante UU du vent correspondant au module maximal du vent trouvé
   (noeuds)
-  Composante VV du vent correspondant au module maximal du vent trouvé
   (noeuds)
-  Niveau de pression PX associé (mb)

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/2/26/Spooki_-_Algorithme_WindMax.pdf

\*Références:\*

-  N/D

\*Mots clés:\*

-  MÉTÉO/WEATHER, vent/wind, maximum, vitesse/speed

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindMax/testsFiles/inputFile.std] >>
                [WindMax] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

\*\* English

**Description:**

-  ...

\*Iteration method:\*

-  ...

\*Dependencies:\*

-  ...

\*Result(s):\*

-  ...

\*Algorithm:\*

-  ...

\*Reference:\*

-  ...

\*Customizable condition:\*

-  N/A

\*Keywords:\*

-  vent/wind, maximum, vitesse/speed

\*Usage:\*

.. code:: example

.. code:: example

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/WindMax/testsFiles/inputFile.std] >>
                [WindMax] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

| **Uses:**
| **Used by:**

 

 