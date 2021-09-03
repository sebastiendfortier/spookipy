Français
--------

Description:
~~~~~~~~~~~~

Multiplication de chaque élément d'un champ par une valeur donnée

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Un champ météorologique

Résultat(s):
~~~~~~~~~~~~

Le champ météorologique dont chaque élément est multiplié par la valeur
donnée

Algorithme:
~~~~~~~~~~~

Soit F, un champ de n éléments Soit z, une valeur donnée par la clé
"value" Pour chaque point faire F(n) = F(n) \* z n >= 1 Fin faire

Références:
~~~~~~~~~~~

Ne s'applique pas

Mots clés:
~~~~~~~~~~

UTILITAIRE/UTILITY, multiplier/multiply

Usage:
~~~~~~

#. Exemple d'appel:

   python3 import fstpy.all as fstpy import spookipy.all as spooki
   records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
   "/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std").to:sub:`pandas`\ ()
   records=MultiplyElementBy(records ,value=10)()
   fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Codé par : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

Multiplies each element of a field by a given value

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

A meteorological field

Result(s):
~~~~~~~~~~

The meteorological field to which the given value has multiplied each
element

Algorithm:
~~~~~~~~~~

For F, a field of n elements For z, a value given by the "value" key for
each point do F(n) = F(n) \* z n >= 1 end do

Reference:
~~~~~~~~~~

Does not apply

Keywords:
~~~~~~~~~

UTILITAIRE/UTILITY, multiplier/multiply

Usage:
~~~~~~

#. Call example:

   python3 import fstpy.all as fstpy import spookipy.all as spooki
   records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
   "/pluginsRelatedStuff/MultiplyElementBy/testsFiles/inputFile.std").to:sub:`pandas`\ ()
   records=MultiplyElementBy(records ,value=10)()
   fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Contacts:
~~~~~~~~~

Author : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Coded by : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
