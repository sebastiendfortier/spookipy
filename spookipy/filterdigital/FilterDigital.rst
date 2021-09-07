Français
--------

**Description:**

-  Appliquer un filtre digital de type Stencil sur un jeu de données.
-  Le filtre, appliqué en un point donné, dans une des directions du
   champ donné, se caractérise par une liste de poids (nombre impair)
   symétriques par rapport au point considéré, et par le nombre de fois
   où celui-ci est appliqué.
-  Le filre est appliqué successivement dans chacune des directions du
   champ donné.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique sur une grille.

\*Résultat(s):\*

-  Les valeurs du champ météorologique filtrées.

\*Algorithme:\*

    Soit F, un champ donné de composantes F(i), dans la direction NI
    (i=1, NI).

    | Soit :math:`\mbox{ $w_n$}`, (n=1,N), une liste de N poids associés
      au filtre digital appliqué sur le champ F, dont le résultat
      :math:`\mbox{
      $F^*$}` sur chaque composante,
    | s'exprime selon :

    :math:`\mbox{ $F^*(i) = \frac {\sum_{n=1}^{N} w_n F(i -
    {\scriptstyle[\frac{N+1}{2}- n]})}{\sum_{n=1}^{N} w_n}$}`    
    :math:`\mbox{ $, 2 \leq i \leq NI-1$}`

    Cette opération est répétée (clé "repetitions"), dans la direction
    NI, autant de fois que le nombre spécifié en paramètre.

    On procède de la même façon dans chaque direction du champ F,
    successivement.

    ***Note:*** : Dans le cas d'un champ 2D, l'algorithme est d'abord
    appliqué dans la direction NI, puis dans la direction NJ.

**Références:**

-  `Inspiré de la fonction FILTRE (*stenfilt.f*) de l'utilitaire
   PGSM <https://wiki.cmc.ec.gc.ca/images/d/dc/Spooki_-_Filtre_html.pdf>`__

\*Mots clés:\*

-  UTILITAIRE/UTILITY, filtre/filter, digital, stencil

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/FilterDigital/testsFiles/inputFile.std] >>
                [FilterDigital --filter 1,2,1 --repetitions 2] >>
                [WriterStd     --output /tmp/$USER/outputFile.std]"
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

-  Apply a digital filter of Stencil type on a data set.
-  The filter, applied on one given point, in one direction of the given
   field, is characterized by a list of weights (odd number) symmetrical
   to the considered point and to the number of times it is applied.
-  The filter is applied successively in each direction of the given
   field.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  A meteorological field on a grid.

\*Result(s):\*

-  The filtered values of the meteorological field.

\*Algorithm:\*

    For F, a given field of components F(i), in the direction NI
    (i=1,NI).

    For :math:`\mbox{ $w_n$}`, (n=1,N), a list of N weights associated
    to the digital filter applied on the F field, which the result
    :math:`\mbox{
    $F^*$}` on each component is expressed as :

    :math:`\mbox{ $F^*(i) = \frac {\sum_{n=1}^{N} w_n F(i -
    {\scriptstyle[\frac{N+1}{2}- n]})}{\sum_{n=1}^{N} w_n}$}`    
    :math:`\mbox{ $, 2 \leq i \leq NI-1$}`

    This operation is repeated ("repetitions" key), in the direction NI,
    as many times as the specified number in parameter.

    We proceed in the same way in each direction of the F field,
    successively.

    ***Note:*** : in the case of a 2D field, the algorithm is first
    applied in the direction NI, and then in the direction NJ.

**Reference:**

-  `Inspired from the FILTRE function (stenfilt.f) of the PGSM
   utility <https://wiki.cmc.ec.gc.ca/images/d/dc/Spooki_-_Filtre_html.pdf>`__

\*Keywords:\*

-  UTILITAIRE/UTILITY, filtre/filter, digital, stencil

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd     --input $SPOOKI_DIR/pluginsRelatedStuff/FilterDigital/testsFiles/inputFile.std] >>
                [FilterDigital --filter 1,2,1 --repetitions 2] >>
                [WriterStd     --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Hatem
   Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 

 