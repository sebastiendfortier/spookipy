Français
========

**Description:**

-  Interpolation horizontale d'un ou plusieurs champ(s) sur une grille
   cible
-  La grille cible peut être soit définie par l'usager, selon les
   paramètres données en option, soit correspondre à la grille d'un des
   champs donnés en entrée
-  Les champs peuvent être scalaires (ex: température) ou vectoriels
   (ex: vent horizontal)

\*/`Notes:/*\\\ <Notes:/*\\>`__

-  Seul le vent peut être interpolé vectoriellement
-  Ne traite que les grilles qui sont définies comme dans les fichiers

standards

-  Interpolation sur grilles de type Y ou Z, définie par l'usager, non

disponible pour le moment

**Méthode d'itération:**

-  Point par point

**Dépendances:**

-  Un ou plusieurs champ(s) sur une ou plusieurs grille(s) source(s)
-  Avec l'option –outputGridDefinitionMethod FIELD\ :sub:`DEFINED`: Un
   champ

| sur une grille cible dont le nom est différent de(s) champ(s) sur
  la/les grille(s) source(s)
| **Résultat(s):**

-  Un ou plusieurs champ(s) interpolé(s) sur une grille cible

**Algorithme:**

-  Détecte la nature scalaire ou vectorielle du champ entré sur la

grille source

-  Appelle les routines scalaires ou vectorielles de la librairie

EZSCINT selon la nature des champs et des clés paramétrables,
appropriées à la grille cible

-  Retourne le champ interpolé sur la grille cible

**Références:**

-  [[http://web-mrb.cmc.ec.gc.ca/science/si/eng/si/misc/grilles.html][Documentation

sur les différents types de grilles supportées]]

-  [[https://wiki.cmc.ec.gc.ca/wiki/Librmn/ezscint][Librairie EZSCINT

de RMNLIB]]

**Mots clés:**

-  INTERPOLATION, extrapolation, horizontale/horizontal, grille/grid,

ezscint

**Usage:**

\*/`Notes:/*\\\ <Notes:/*\\>`__ Pour la clé
'–outputGridDefinitionMethod':

-  FIELD\ :sub:`DEFINED`: la grille cible est définie à l'aide du champ
   identifié par l'option –fieldName. Attention: le champ ainsi
   identifié ne doit être disponible que sur une grille unique.
-  USER\ :sub:`DEFINED`: la grille cible est définie en fonction des
   valeurs des clés paramétrables –gridType, –xyDimensions et
   –gridProjectionParameters. Voir la documentation sur les fichiers
   standards et les grilles supportées dans les références, pour
   l'utilisation de ces clés

Pour la clé '–interpolationType':

-  NEAREST: la valeur interpolée en un point de la grille cible est
   obtenue par la valeur du point le plus proche de la grille source
-  BI-LINEAR: interpolation bi-linéaire
-  BI-CUBIC: interpolation bi-cubique

Pour la clé '–extrapolationType':

-  NEAREST: les valeurs à l'extérieur du domaine sont remplacées par les
   valeurs des plus proches voisins à l'intérieur du domaine
-  LINEAR: extrapolation linéaire
-  MAXIMUM: les valeurs à l'extérieur du domaine sont remplacées par la
   valeur maximum du champ à laquelle est ajouté 5% de sa variation
   totale
-  MINIMUM: les valeurs à l'extérieur du domaine sont remplacées par la
   valeur minimum du champ à laquelle est soustrait 5% de sa variation
   totale
-  VALUE: les valeurs à l'extérieur du domaine sont remplacées par une
   valeur numérique donnée (float)
-  ABORT: abandon de la requête

**Exemple d'appel:**

::

   ...
   spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalGrid/testsFiles/inputFile.std] >>
               [InterpolationHorizontalGrid --outputGridDefinitionMethod USER_DEFINED
                                               --gridType TYPE_N
                                               --xyDimensions 191,141
                                               --gridProjectionParameters 79.0,117.0,57150.0,21.0
                                               --interpolationType BI-LINEAR
                                               --extrapolationType VALUE=99.9] >>
               [WriterStd --output /tmp/$USER/outputFile.std]"
   ...

-  `Autres
   exemples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Exemples#Exemple_d.27interpolation_horizontale_sur_grille>`__

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à
`InterpolationHorizontalGrid <InterpolationHorizontalGrid_8cpp.html>`__.

Tests unitaires

| \*Ce plugin utilise:\*
| \*Ce plugin est utilisé par:\*

English
=======

**Description:**

-  voir
   `c\ ezsint <http://web-mrb.cmc.ec.gc.ca/mrb/si/eng/si/libraries/rmnlib/ezscint/>`__

**Iteration method:**

-  N/A

**Dependencies:**

-  N/A

**Result(s):**

-  N/A

**Algorithm:**

-  N/A

**References:**

-  `Grid types supported by RPN Standard
   Files <http://web-mrb.cmc.ec.gc.ca/science/si/eng/si/misc/grilles.html>`__

**Customizable condition:**

-  N/A

**Keywords:**

-  interpolateur/interpolator, interpolation,
   extrapolateur/extrapolator, extrapolation, horizontale/horizontal

**Usage:**

**Call example:**

::

   ...
   spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationHorizontalGrid/testsFiles/inputFile.std] >>
               [InterpolationHorizontalGrid --outputGridDefinitionMethod USER_DEFINED
                                               --gridType TYPE_N
                                               --xyDimensions 191,141
                                               --gridProjectionParameters 79.0,117.0,57150.0,21.0
                                               --interpolationType BI-LINEAR
                                               --extrapolationType VALUE=99.9] >>
               [WriterStd --output /tmp/$USER/outputFile.std]"
   ...

-  `Other
   examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Example_of_horizontal_interpolation>`__

**Results validation:**

-  Under construction!

**Contacts:**

-  Author : `Maryse
   Beauchemin <https://wiki.cmc.ec.gc.ca/wiki/User:Beaucheminm>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| \*Uses:\*
| \*Used by:\*

 
