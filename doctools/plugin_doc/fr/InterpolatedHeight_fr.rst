Français
--------

**Description:**

-  Déterminer la hauteur géopotentielle interpolée linéairement entre
   deux niveaux verticaux

\*Méthode d'itération:\*

-  colonne par colonne

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  La hauteur géopotentielle interpolé GZ

\*Algorithme:\*

-  https://wiki.cmc.ec.gc.ca/images/c/c3/Spooki_-_Algorithme_HauteurInterpol_v1.1.doc

\*Références:\*

-  Le programme opérationnel
   https://wiki.cmc.ec.gc.ca/images/3/36/Spooki_-_Programme_Operationnel_CloudAmountAndLevel_Ecldcig_fstd2000.f

\*Mots clés:\*

-  INTERPOLATION, linéaire/linear, niveau/level, vertical,
   hauteur/height, géopotentielle/geopotential

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolatedHeight/testsFiles/inputFile.std] >>
                [InterpolatedHeight --inputFieldName CLD --threshold 0.6] >>
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

Tests Unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
