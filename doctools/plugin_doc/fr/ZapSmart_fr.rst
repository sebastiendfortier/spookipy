Français
--------

**Description:**

-  Permet de sélectionner et de renommer une ou plusieurs valeur(s)
   d'attribut(s) de champ(s) dans la structure interne de mémoire
-  Les clés paramétrables sont déclarées en paires de la forme : from ->
   to

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Au moins un attribut de la structure interne de mémoire

\*Résultat(s):\*

-  Un ou plusieurs champ(s) dont les valeur(s) d'attributs sont
   sélectionnée(s) et renommée(s) selon les arguments passés dans les
   clés paramétrables

\*Algorithme:\*

.. code:: example

    Sélectionne une ou plusieurs attribut(s) du champ dans la structure de mémoire à l'aide du plugin "Select"
    Modifie le ou les valeur(s) d'attribut(s) à l'aide du plugin "Zap"
    Sélectionne les autres attributs du champ à l'aide du plugin "Select" et de la clé paramétrable "exclude" afin de les conserver intacts

**Références:**

-  `Composantes de la structure interne de
   mémoire <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Composantes_du_syst%C3%A8me#meteo_infos:>`__
-  [[https://wiki.cmc.ec.gc.ca/wiki/Spooki/Correspondance_Fichiers_STD_-_SPOOKI][Correspondance
   entre les descripteurs d'enregistrements de fichiers standards et les
   attributs de la mémoire interne de SPOOKI]]

\*Mots clés:\*

-  SYSTÈME/SYSTEM, zap, renommer/rename

\*Usage:\*

    \*/\ `Notes:/\*\\\\ <Notes:/*\\>`__ Lorsque plusieurs clés
    paramétrables sont spécifiées dans la même requête de , la requête
    agit strictement sur les champs répondant à tous les critères de
    sélections passés à travers les clés paramétrables --\*From (ex.
    --fieldNameFrom TT --pdsLabelFrom ETIKET --forecastHourFrom 12 =>
    pour que la requête soit un succès, il faut absolument avoir: au
    moins un champ appelé TT, à l'heure de prévision 12 et ayant pour
    étiquette ETIKET).

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/ZapSmart/testsFiles/inputFile.std] >>
                [ZapSmart --fieldNameFrom VV --fieldNameTo UU] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à `ZapSmart <ZapSmart_8cpp.html>`__.

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
