Français
--------

**Description:**

-  Permet de renommer une ou plusieurs valeur(s) d'attribut(s) de
   champ(s) dans la structure interne de mémoire du système, sans
   altérer les données elles-mêmes.
   ***Note:*** les arguments donnés dans les clés paramétrables
   correspondent aux nouvelles valeurs des attributs

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Au moins un champ dans la structure interne de mémoire

\*Résultat(s):\*

-  Un ou plusieurs champ(s) dont les valeur(s) d'attributs sont
   renommées selon les arguments passés dans les clés paramétrables

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  `Composantes de la structure interne de
   mémoire <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_syst%C3%A8me#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI][Correspondance
   entre les descripteurs d'enregistrements de fichiers standards et les
   attributs de la mémoire interne de SPOOKI]]

\*Mots clés:\*

-  SYSTÈME/SYSTEM, zap, renommer/rename

\*Usage:\*

    \*/\ `Notes:/\*\\\\ <Notes:/*\\>`__ L'argument
    ARBITRARY\ :sub:`CODE` de la clé paramétrable --verticalLevelType
    est utilisé pour désigner un type de niveau vertical qui ne
    correspond à aucun des types mentionnés dans la liste

    La liste de toutes les unités valides est disponible
    `ici <units.html>`__

    Actuellement, aucune distinction n'est possible, entre les niveaux
    ETA et SIGMA, de même qu'entre les niveaux HYBRID et
    HYBRID\ :sub:`STAGGERED`. Par conséquent, l'argument SIGMA de la clé
    paramétrable --verticalLevelType, renommera à la fois des niveaux
    SIGMA et ETA en niveaux SIGMA. De même, l'argument HYBRID renommera
    à la fois des niveaux HYBRID et HYBRID\ :sub:`STAGGERED` en niveaux
    HYBRID.

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Zap/testsFiles/inputFile.std] >>
                [Select --fieldName UU] >>
                [Zap --fieldName FF --pdsLabel WINDMODULUS --typeOfField ANALYSIS --dateOfOrigin 20080529133415
                --forecastHour 144 --userDefinedIndex 66 --unit scalar] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
