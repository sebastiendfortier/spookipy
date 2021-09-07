Français
--------

**Description:**

-  À un niveau donné, le programme convertit les valeurs d'humidité
   relative (HR) en fraction nuageuse diagnostique au moyen d'une
   formule issue des travaux de Slingo (1987). Le calcul de la fraction
   nuageuse dépend de HR et d'une valeur empirique seuil pouvant varier
   à la verticale.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  HR : Humidité relative (sans unité, entre 0 et 1).

\*Résultat(s):\*

-  Le champ fraction nuageuse diagnostique en chaque point de grille,
   champ en 3D. Sans unité, entre 0 et 1. CLD

\*Algorithme:\*

-  http://iweb.cmc.ec.gc.ca/~afsyyah/Algorithme_DiagnostiqueCloudFraction_v1.1.doc

\*Références:\*

-  https://wiki.cmc.ec.gc.ca/images/6/6f/Spooki_-_Slingo_1987.pdf
-  https://wiki.cmc.ec.gc.ca/images/e/e6/Spooki_-_McFarlane_et_al_1992.pdf

\*Mots clés:\*

-  MÉTÉO/WEATHER, fraction, nuageu/cloudy, nuage/cloud,
   diagnostique/diagnostic, slingo

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/CloudFractionDiagnostic/testsFiles/inputFile.std] >>
                [CloudFractionDiagnostic] >>
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
`CloudFractionDiagnostic <CloudFractionDiagnostic_8cpp.html>`__.

Tests Unitaires

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

\*Keywords:\*

-  ...

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd    --input $SPOOKI_DIR/pluginsRelatedStuff/CloudFractionDiagnostic/testsFiles/inputFile.std] >>
                [CloudFractionDiagnostic] >>
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

 