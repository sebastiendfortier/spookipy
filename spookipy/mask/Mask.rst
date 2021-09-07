Français
--------

Description:
~~~~~~~~~~~~

Ce plugin crée un masque selon la(les) valeur(s) et seuil(s) demandés.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Un champ

Résultat(s):
~~~~~~~~~~~~

Champ MASK

Algorithme:
~~~~~~~~~~~

Soit F, un champ d'entrée Soit opérateur[j], j ième valeur donnée dans
la liste de la clé ,operators= Soit seuil[j], j ième valeur donnée dans
la liste de la clé ,thresholds= Soit valeur[j], j ième valeur donnée
dans la liste de la clé ,values= Soit MASK, le champ en sortie Soit
nbTrios, le nombre total de trios de seuil, opérateur, valeur Pour
chaque point du champ d'entrée (i) Initialiser le champ MASK[i] = 0.0
Pour j de 0 à (nbTrios-1) Si F[i] opérateur[j] seuil[j] MASK[i] =
valeur[j] Fin Si Fin Pour Fin Pour

Références:
~~~~~~~~~~~

Ne s'applique pas

Mots clés:
~~~~~~~~~~

UTILITAIRE/UTILITY, masque/mask

Usage:
~~~~~~

#. Exemple d'appel:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/Mask/testsFiles/inputFile.std") ()
       records=Mask(records ,thresholds=0.0,10.0,15.0,20.0 ,values=0.0,10.0,15.0,20.0 ,operators=GE,GE,GE,GE)()
       StandardFileWriter("/tmp/"+USER+"/outputFile.std --noUnitConversion",records).compute()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) :

-  `Marc Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__
-  `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__

Codé par : `Louise Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Faustl>`__
Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

This plug-in creates a mask according to the threshold value(s) given.

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

A field

Result(s):
~~~~~~~~~~

MASK field

Algorithm:
~~~~~~~~~~

For F, an input field For thresholds[j], jth value given in the list of
,thresholds=option For operator[j], jth value given in the list of
,operators=option For value[j], jth value given in the list of
,values=option For nbTrios, the total number of threshold, operator and
value trios For each point of the input field (i) Initialize MASK = 0.0
For j = 0 to (nbTrios1) If F[i] Operators[j] Thresholds[j]
MASK[i]=Value[j] Endif End for End for

Reference:
~~~~~~~~~~

Does not apply

Keywords:
~~~~~~~~~

UTILITAIRE/UTILITY, masque/mask

Usage:
~~~~~~

#. Call example:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/Mask/testsFiles/inputFile.std") ()
       records=Mask(records ,thresholds=0.0,10.0,15.0,20.0 ,values=0.0,10.0,15.0,20.0 ,operators=GE,GE,GE,GE)()
       StandardFileWriter("/tmp/"+USER+"/outputFile.std --noUnitConversion",records).compute()

Contacts:
~~~~~~~~~

Auteur(e) :

-  `Marc Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__
-  `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__

Codé par : `Louise Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Faustl>`__
Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__