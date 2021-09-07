Français
--------

**Description:**

-  Copie le champ passé en entrée et remplace toutes ses valeurs par une
   constante donnée. Possibilité de générer un champ 2D constant à
   partir d'un champ 3D.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Un champ météorologique

\*Résultat(s):\*

-  Une copie (3D ou 2D) du champ météorologique passé en entrée
   contenant la valeur passée en paramètre.

\*Algorithme:\*

-  Ne s'applique pas

\*Références:\*

-  Ne s'applique pas

\*Mots clés:\*

-  UTILITAIRE/UTILITY, constant, generate/produire

\*Usage:\*

    \*/\ `Notes:/\*\\\\ <Notes:/*\\>`__ Pour la clé '--value':

    -  MAXINDEX: la valeur de l'indice du dernier niveau du champ
       d'entrée
    -  MININDEX: la valeur de l'indice du premier niveau du champ
       d'entrée
    -  NBLEVELS: le nombre de niveaux du champ d'entrée

    \*Exemple d'appel:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SetConstantValue/testsFiles/inputFile.std] >>
                    [SetConstantValue --value 4.0] >>
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

    Voir la référence à

    `Tests unitaires <SetConstantValueTests_8cpp.html>`__

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
