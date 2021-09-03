Français
--------

**Description:**

-  Calcul du niveau de condensation par ascendance (NCA ou LCL en
   anglais), basé sur la température , le point de rosée et la pression
   d'un niveau donné. Le NCA est défini comme la hauteur à laquelle une
   parcelle d'air soumise à un soulèvement adiabatique sec atteint le
   niveau de saturation. Ce niveau peut être trouvé graphiquement sur un
   diagramme thermodynamique (tephigram) en suivant l'adiabatique sèche
   et la ligne de rapport de mélange constant jusqu'au point
   d'intersection.
-  Le plugin est conçu de façon générique pour qu'il s'applique à
   n'importe quelle parcelle telle qu'une soulevée de la surface, une
   représentée par la moyenne d'une couche, la parcelle la plus instable
   et/ou toute(s) autre(s) parcelle(s) définie(s) par l'usager.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air au niveau de la parcelle à être soulevée, TT
-  Hauteur géopotentielle de la surface, GZ
   (ou GZG si GZ à la surface n'est pas disponible)
-  Hauteur géopotentielle de la parcelle à être soulevée, GZ
   **et** un des champs suivants:
-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Température du point de rosée, TD
-  Écart du point de rosée, ES
-  Humidité relative, HR
   ***Note:*** Assurez-vous de fournir à ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s):\*

-  TLCL (deg C), température au niveau de condensation par ascendance,
   encore appelée température de saturation
   ou MTCL (deg C) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
   ou UTCL (deg C) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
-  PLCL (hPa), pression au niveau de condensation par ascendance
   ou MPCL (hPa) si on utilise "--liftedFrom MEAN\ :sub:`LAYER`"
   ou UPCL (hPa) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"
-  ZLCL (m), hauteur du niveau de condensation par ascendance à partir
   de la surface,
   ou MZCL (m) si on utilise "--lifterFrom MEAN\ :sub:`LAYER`"
   ou UZCL (m) si on utilise "--liftedFrom MOST\ :sub:`UNSTABLE`"

| \*Algorithme:\*

-  `Algorithme pour LevelOfCondensationByLifting (présentement en
   Anglais) <https://wiki.cmc.ec.gc.ca/images/d/d8/SPOOKI_-_Algorithme_LevelOfCondensationByLifting.docx>`__

\*Références:\*

-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281968%29007%3C0511%3AAESTTC%3E2.0.CO%3B2][Barnes,
   S. L., 1968: An empirical shortcut to the calculation of temperature
   and pressure at the lifted condensation level.]]
-  Bolton, D. 1980: The computation of equivalent potential temperature.
   *Mon. Wea. Rev*., 108, 1046-1053. `Disponible en
   ligne <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0493%281980%29108%3C1046%3ATCOEPT%3E2.0.CO%3B2>`__
   ou
   `localement <https://wiki.cmc.ec.gc.ca/images/1/1a/Spooki_-_Bolton1980.pdf>`__
-  [[http://iweb.cmc.ec.gc.ca/%7Eafsypst/info_divers/doc_thermo.pdf][Brunet,
   N., 2001: Les Fonctions Thermodynamiques et le Fichier de
   Constantes.]]
-  "Atmospheric Thermodynamics", Iribarne, J.V., and Godson, W.L.
   (Riedel, 2nd edition, 1981)
-  `Atmospheric Convection, Kerry A., Emanuel,
   1994 <http://books.google.ca/books?id=VdaBBHEGAcMC&dq=atmospheric+convection+Kerry+A+Emanuel&printsec=frontcover&source=bn&hl=en&ei=WsWsS7GEONKUtgf9rKHCDw&sa=X&oi=book_result&ct=result&safe=images&redir_esc=y#v=onepage&q&f=false>`__
-  `Librairie thermodynamique de
   RPN <http://iweb.cmc.ec.gc.ca/%7Eafsypst/info_divers/doc_thermo.pdf>`__

\*Mots clés:\*

-  MÉTÉO/WEATHER, condensation, ascendance/lifting, saturation,
   convection

\*Usage:\*

    | 
    | **Informations sur les métadonnées :**
    | Lorsque les options --MeanLayer et --MostUnstable sont utilisées:

    -  Le verticalLevel (IP1 dans les fichiers RPN STD) indiquera la
       base de la couche moyenne ou la base de recherche pour la couche
       la plus instable.
    -  Les caractères 2 à 4 du pdsLabel (5 à 8 de l'etiket dans les
       fichiers RPN STD) indiqueront l'épaisseur de la couche moyenne ou
       l'épaisseur de la couche la plus instable. Le dernier de ces
       caractères indique l'unité (P pour hPa au-dessus de la base de la
       couche, Z pour mètres au-dessus de la base de la couche).

    \*Exemple d'appel:\*

    .. code:: example

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/LevelOfCondensationByLifting/testsFiles/inputFile.std] >>
                    [LevelOfCondensationByLifting --outputField TEMPERATURE --liftedFrom SURFACE --iceWaterPhase WATER] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

    **Validation des résultats:**

    **Contacts:**

    -  Auteur(e) : Neil Taylor
    -  Codé par : Jonathan Cameron
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Voir la référence à

    Tests unitaires

    | **Ce plugin utilise:**
    | **Ce plugin est utilisé par:**

     
