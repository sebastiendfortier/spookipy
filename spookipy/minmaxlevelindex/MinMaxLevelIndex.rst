Français
--------

Description:
~~~~~~~~~~~~

Trouve l'indice de la valeur maximale et/ou minimale dans une colonne,
ou une partie de celle-ci.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Colonne par colonne

Dépendances:
~~~~~~~~~~~~

-  Champ météorologique (3D)

Si la clé ,bounded=est activée:

-  Champ d'indices de la limite inférieure, KBAS (2D)
-  Champ d'indices de la limite supérieure, KTOP (2D)

Résultat(s):
~~~~~~~~~~~~

Un champ d'indices, KMIN(2D), pour lesquels la valeur du champ
météorologique est minimale et/ou Un champ d'indices, KMAX(2D), pour
lesquels la valeur du champ météorologique est maximale

Algorithme:
~~~~~~~~~~~

.. code:: example

    Si la clé ,bounded=n'est pas activée:
    KBAS = niveau le plus bas de la colonne 
    KTOP = niveau le plus haut de la colonne 
    Pour chaque colonne et pour les niveaux avec l'indice entre KBAS et KTOP 
    Si la clé ,minMax== MIN ou BOTH 
    boucle k = KBAS à KTOP 
    Si minVAR[k] alors 
    min= VAR[k] et KMIN=k 
    Si la clé ,minMax== MAX ou BOTH 
    boucle k = KBAS à KTOP 
    Si max < VAR[k] alors 
    max = VAR[k] et KMAX=k

Références:
~~~~~~~~~~~

Aucune

Mots clés:
~~~~~~~~~~

UTILITAIRE/UTILITY, minimum, maximum, niveau/level,
vertical,borné/bounded

Usage:
~~~~~~

#. Exemple d'appel:

   .. code:: python

       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std").to_pandas()
       records=spooki.MinMaxLevelIndex(records ,min=True, ascending=True).compute()
       fstpy.StandardFileWriter("/tmp/"+USER+"/outputFile.std",records).to_fst()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Responsables:
~~~~~~~~~~~~~

Auteur(e) :

-  `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__

Codé par :

-  `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Jonathan Cameron

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

Finds the index of the maximum, minimum value or both in the column or
part of it.

Iteration method:
~~~~~~~~~~~~~~~~~

Column by column

Dependance:
~~~~~~~~~~~

Meteorological field (3D) If the ,bounded=key is activated: Field of
indexes of the lower limit, KBAS Field of indexes of the upper limit,
KTOP

Result(s):
~~~~~~~~~~

A field with the indexes where the value of the meteorological field is
minimum, KMIN <br /> and/or A field with the indexes where the value of
the meteorological field is maximum, KMAX

Algorithm:
~~~~~~~~~~

If the key ,bounded=is not activated : KBAS = lowest level in the column
KTOP = highest level in the column For each column and for the levels
between KBAS and KTOP: if key ,minMax== MIN or BOTH loop for k between
KBAS and KTOP if minVAR[k] then min = VAR[k] and KMIN = k if key
,minMax== MAX or BOTH loop for k between KBAS and KTOP if max < VAR[k]
then max = VAR[k] and KMAX = k

Reference:
~~~~~~~~~~

Keywords:
~~~~~~~~~

minimum, maximum, niveau/level, vertical, borné/bounded

Usage:
~~~~~~

#. Call example:

   .. code:: python

       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std").to_pandas()
       records=MinMaxLevelIndex(records ,minMax=MIN ,direction=UPWARD)()
       .StandardFileWriter("/tmp/"+USER+"/outputFile.std",records).to_fst()
       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std").to_pandas()
       ( [Copy] + ( ([SetConstantValue ,value=MININDEX --bidimensional]  >
       records=zap(records ,nomvar=KBAS]) + ([SetConstantValue
       ,value=MAXINDEX --bidimensional] [zap ,nomvar=KTOP)()  >
       records=MinMaxLevelIndex(records ,bounded=,minMax=MIN
       ,direction=DOWNWARD)()  >
       fstpy.StandardFileWriter("/tmp/"+USER+"/outputFile.std",records).to_fst()

Responsables:
~~~~~~~~~~~~~

Author :

-  `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__

Coded by :

-  `Sébastien Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
-  Jonathan Cameron

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
