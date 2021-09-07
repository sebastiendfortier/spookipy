Français
--------

**Description:**

-  Calcul de l'helicite relative, outil necessaire pour la prevision des
   orages violents

\*Méthode d'itération:\*

-  Integration sur une colonne d'air verticale (1D)

\*Dépendances:\*

-  Composante du Vent zonale UU (m/s) (par rapport au nord)
-  Composante du Vent meridionale VV (m/s) (par rapport au nord)
-  Composante du Vent UV (m/s)
-  La direction du vent WD (deg)
-  La hauteur geopotentielle GZ (Km)

\*Résultat(s):\*

-  HL : Helicite relative (m\*\*2/s\*\*2)

\*Algorithme:\*
https://wiki.cmc.ec.gc.ca/images/8/82/Spooki_-_Algorithme_Helicity.pdf

**Références:**

-  

   #. Article de reference :

   https://wiki.cmc.ec.gc.ca/images/c/c3/Spooki_-_Helicity_Characteristics.pdf
-  

   #. Demonstration:

   https://wiki.cmc.ec.gc.ca/images/1/18/Spooki_-_Helicity.pdf

\*Conditions paramétrable:\*

-  Z3 = niveau vertical correspond a ~850 mb
-  Z4 = niveau vertical correspond a ~300 mb

\*Mots clés:\*

-  MÉTÉO/WEATHER, sévère/severe, été/summer, aviation, tornade/tornado,
   énergie/energy, éolienne

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Helicity/testsFiles/inputFile.std] >>
                [Helicity] >>
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

English
-------

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

-  ...

\*Keywords:\*

-  ...

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Helicity/testsFiles/inputFile.std] >>
                [Helicity] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

-  ...

\*Contacts:\*

-  ...

Reference to

Tests unitaires

| **Uses:**
| **Used by:**
