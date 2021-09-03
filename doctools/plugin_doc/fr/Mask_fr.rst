Français
--------

**Description:**

-  Ce plugin crée un masque selon la(les) valeur(s) et seuil(s)
   demandés.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ

\*Résultat(s):\*

-  Champ MASK

\*Algorithme:\*

.. code:: example

    Soit F,            un champ d'entrée
    Soit opérateur[j], j ième valeur donnée dans la liste de la clé --operators
    Soit seuil[j],     j ième valeur donnée dans la liste de la clé --thresholds
    Soit valeur[j],    j ième valeur donnée dans la liste de la clé --values
    Soit MASK,         le champ en sortie
    Soit nbTrios,      le nombre total de trios de seuil, opérateur, valeur

    Pour chaque point du champ d'entrée (i)

       Initialiser le champ MASK[i] = 0.0

       Pour j de 0 à (nbTrios-1)

           Si F[i]  opérateur[j]  seuil[j]
              MASK[i] = valeur[j]
           Fin Si

       Fin Pour

    Fin Pour

**Références:**

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, masque/mask

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Mask/testsFiles/inputFile.std] >> 
                [Mask --thresholds 0.0,10.0,15.0,20.0 --values 0.0,10.0,15.0,20.0 --operators GE,GE,GE,GE] >> 
                [WriterStd --output /tmp/$USER/outputFile.std --noUnitConversion]"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__, / `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__
-  Codé par : `Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Faustl>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à .

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
