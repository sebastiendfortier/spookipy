Français
--------

**Description:**

-  Sélectionne parmi les champs spécifiés celui ayant le plus grand
   nombre de niveaux communs avec le champ de référence donné.

\*Méthode d'itération:\*

-  Ne s'applique pas.

\*Dépendances:\*

-  Au moins deux champs en entrée.

\*Résultat(s):\*

-  Le champ ayant le plus grand nombre de niveaux communs avec le champ
   de référence.
-  Le champ de référence.

\*Algorithme:\*

.. code:: example

    - Trouver parmi les champs donnés selon la clé paramètrable --matchFields celui ayant le plus de niveaux verticaux en commun avec le champ de référence.

    - Retourner ce champ avec le champ de référence sur les niveaux communs.

**Références:**

-  Aucune.

\*Mots clés:\*

-  UTILITAIRE/UTILITY, sélection/selection, correspondance/match,
   niveaux/levels

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MatchFieldsByCommonLevels/testsFiles/inputFile.std] >>
                [MatchFieldsByCommonLevels --referenceField TT --matchFields HU,HR,ES,TD] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Codé par : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
