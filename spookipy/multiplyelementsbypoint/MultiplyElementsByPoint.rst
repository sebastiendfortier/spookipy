Français
--------

Description:
~~~~~~~~~~~~

Multiplication en chaque point des valeurs de tous les champs reçus

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Au moins 2 champs différents

Résultat(s):
~~~~~~~~~~~~

Un champ nommé "MUEP" avec le résultat de la multiplication des champs
d'entrée.

Algorithme:
~~~~~~~~~~~

MUEP[i,j,k] = A[i,j,k] \* B[i,j,k] \*

Références:
~~~~~~~~~~~

Ne s'applique pas

Mots clés:
~~~~~~~~~~

UTILITAIRE/UTILITY, grille/grid, point, multiplier/multiply,
produit/product

Usage:
~~~~~~

Exemple d'appel: python3 import fstpy.all as fstpy import spookipy.all
as spooki records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
"/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std").to:sub:`pandas`\ ()
s=MultiplyElementsByPoint(records).compute()
fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ Codé par :
`Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
`Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__ Support
: `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__ Ce plugin est utilisé
par:

English
-------

Description:
~~~~~~~~~~~~

Multiplication of the values of all the fields received at each point

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

At least 2 different fields

Result(s):
~~~~~~~~~~

A field named "MUEP" with the result of the multiplication of the input
fields

Algorithm:
~~~~~~~~~~

MUEP[i,j,k] = A[i,j,k] \* B[i,j,k] \*

Reference:
~~~~~~~~~~

Does not apply

Keywords:
~~~~~~~~~

UTILITAIRE/UTILITY, grille/grid, point, multiplier/multiply,
produit/product

Usage:
~~~~~~

#. Call example:

   python3 import fstpy.all as fstpy import spookipy.all as spooki
   records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
   "/pluginsRelatedStuff/MultiplyElementsByPoint/testsFiles/inputFile.std").to:sub:`pandas`\ ()
   s=MultiplyElementsByPoint(records).compute()
   fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Contacts:
~~~~~~~~~

Author : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ Coded by :
`Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
`Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
