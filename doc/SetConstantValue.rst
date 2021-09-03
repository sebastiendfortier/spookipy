Français
--------

Description:
~~~~~~~~~~~~

Copie le champ passé en entrée et remplace toutes ses valeurs par une
constante donnée. Possibilité de générer un champ 2D constant à partir
d'un champ 3D.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Un champ météorologique

Résultat(s):
~~~~~~~~~~~~

Une copie (3D ou 2D) du champ météorologique passé en entrée contenant
la valeur passée en paramètre.

Algorithme:
~~~~~~~~~~~

Ne s'applique pas

Références:
~~~~~~~~~~~

Ne s'applique pas

Mots clés:
~~~~~~~~~~

UTILITAIRE/UTILITY, constant, generate/produire

Usage:
~~~~~~

Notes:

Pour la clé '--value':
~~~~~~~~~~~~~~~~~~~~~~

MAXINDEX:la valeur de l'indice du dernier niveau du champ d'entrée
MININDEX:la valeur de l'indice du premier niveau du champ d'entrée
NBLEVELS:le nombre de niveaux du champ d'entrée Exemple d'appel: python3
import fstpy.all as fstpy import spookipy.all as spooki
records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
"/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std").to:sub:`pandas`\ ()
records=SetConstantValue(records ,value=4.0)()
fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ Codé par :
`Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__ Ce plugin est utilisé
par:

English
-------

Description:
~~~~~~~~~~~~

Copy the input field and replace all its values by a given constant.
Possibility to generate a 2D constant field from a 3D field.

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

A meteorological field

Result(s):
~~~~~~~~~~

A copy (3D or 2D) of the meteorological field received from input
containing the value received as parameter

Algorithm:
~~~~~~~~~~

Does not apply

Reference:
~~~~~~~~~~

None

Keywords:
~~~~~~~~~

UTILITAIRE/UTILITY, constant, generate/produire

Usage:
~~~~~~

Notes:

For the '--value' option:
~~~~~~~~~~~~~~~~~~~~~~~~~

MAXINDEX:the index number of the last level of the input field
MININDEX:the index number of the first level of the input field
NBLEVELS:the number of levels of the input field

#. Call example:

   python3 import fstpy.all as fstpy import spookipy.all as spooki
   records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
   "/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std").to:sub:`pandas`\ ()
   records=SetConstantValue(records ,value=4.0)()
   fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Contacts:
~~~~~~~~~

Author : `Sébastien
Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__ Coded by :
`Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
