Français
--------

**Description:**

-  Calculatrice

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Au moins un champ dans la structure interne de mémoire

\*Résultat(s):\*

-  Un champ

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  `Composantes de la structure interne de
   mémoire <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_système#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI][Correspondance
   entre les descripteurs d'enregistrements de fichiers standards et les
   attributs de la mémoire interne de SPOOKI]]

\*Mots clés:\*

-  SYSTÈME/SYSTEM, calculatrice/calculator **Usage:**

\*Exemple d'appel:\*

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Calculator/testsFiles/srcFile2.std] >>
                [Select --fieldName TT ] >> [Zap --tag tt] >> [Calculator --expression *7 --unit celsius --outputFieldName TT7] >>
                [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Simon
   Voyer-Poitras <https://wiki.cmc.ec.gc.ca/wiki/User:Voyerpoitrass>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
