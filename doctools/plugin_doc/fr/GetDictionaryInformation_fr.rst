Français
--------

**Attention! Plugin à usage restreint**
=======================================

**Description:**

-  Lecture de dictionnaires utilisés dans le système SPOOKI
-  Chaque base de données est constituée d'une ou plusieurs tables,
   elle(s)-même(s) constituée(s) de plusieurs attributs, eux-mêmes
   contenant plusieurs enregistrements
-  Le contenu des bases de données disponibles peut être consulté
   **`ici <databaseIndex.html>`__**
-  Ce plugin permet de sélectionner les attributs d'une ou plusieurs
   table(s) d'une même base de données spécifiée
-  Possibilité d'utiliser une requête simple, correspondant à
   l'utilisation de la clause "WHERE" du langage SQlite ainsi qu'une
   requête plus complexe correspondant à une commande SQlite directe
   basée sur l'expression "SELECT FROM WHERE"
-  Des exemples d'utilisation de ce plugin sont disponibles
   **`ici <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Exemples#Exemples_d.27interrogation_de_bases_de_donn.C3.A9es_avec_SPOOKI>`__**
   ***Note:*** Pour le moment, seules les tables EXTRASSTATIONS,
   EXTRASSTATIONSRAW, MDICP4D, MDICP4DRAW, PRODUCTS et STATIONSFB de la
   base de données STATIONS.db peuvent être consultées sans risque.

\*Méthode d'itération:\*

-  Ne s'applique pas

\*Dépendances:\*

-  Ne s'applique pas

\*Résultat(s):\*

-  Un ou plusieurs champs contenant les informations demandées et
   portant le nom des arguments de la clé --outputAttribute
-  Ex: La sélection de tous les enregistrements de l'attribut "Latitude"
   de la base de données "MDICP4D" sera un champ portant le nom
   "Latitude"

| \*Algorithme:\*

-  Effectuer une requête SQL sur une base de données et transférer les
   informations reçues dans un ou plusieurs champs
-  Attention : la requête peut échouer si une colonne sélectionnée dans
   une table contient des enregistrements vides

\*Références:\*

-  `SQLite <http://www.sqlite.org/>`__
-  `Dictionnaire principal de stations
   météorologiques <https://wiki.cmc.ec.gc.ca/wiki/Format_du_dictionnaire_de_stations_m%C3%A9t%C3%A9orologiques>`__

\*Mots clés:\*

-  SYSTÈME/SYSTEM, base\ :sub:`dedonnées`/database,
   dictionnaire/dictionary, table

\*Usage:\* \*/\ `Notes:/\*\\\\ <Notes:/*\\>`__

-  Le caractère "\_" est ajouté entre chaque argument pour que la
   syntaxe soit correctement interpretée par le système
-  Utilisation des clés "--table" et "--outputAttribute" dans le cas
   d'une requête SQL directe (clé --advancedRequest) :
     - La clé "--table" n'est pas obligatoire puisque les tables sont
   indiquées directement avec la clause "FROM". Elle est donc simplement
   ignorée par le système
     - Même si, à première vue, les attributs sélectionnés sont indiqués
   directement avec la clause "SELECT", l'utilisation de la clé
   "--outputAttribute" est nécessaire pour éviter toute confusion en cas
   de complexité de la commande SQL entrée en paramètre
-  Syntaxe d'appel de la clé "--subset" : voir
   `ce <https://wiki.cmc.ec.gc.ca/images/b/b0/Spooki_-_Syntaxe_cl%C3%A9_GetDictionary_infos.doc>`__
   document
-  Syntaxe d'appel de la clé "--advancedRequest" : voir la référence sur
   le langage SQlite

\*Exemple d'appel:\*

.. code:: example

    ...
    spooki_run "[GetDictionaryInformation --dataBase STATIONS --outputAttribute TYPE --table CANSTAT] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

-  `Autres
   exemples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Exemples#Exemples_d.27interrogation_de_bases_de_donn.C3.A9es_avec_SPOOKI>`__

\*Validation des résultats:\*

**Contacts:**

-  Auteur(e) : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Codé par : `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
