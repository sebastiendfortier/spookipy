Français
--------

**Description:**

-  Calcul de la température du thermomètre mouillé, température
   qu'atteindrait une parcelle d'air, ayant une température potentielle
   et un contenu en vapeur d'eau donnés, si on évaporait son contenu en
   eau liquide jusqu'à saturation tout en gardant la pression constante.
   ***Note:*** Si la pression est plus petite que 5hPa le calcul ne
   tient pas lieu et TTW est attitré la valeur de -999.

\*Méthode d'itération:\*

-  Point par point

\*Dépendances:\*

-  Température de l'air (TT)
   **et** un des champs suivants:
-  Humidité spécifique, HU
-  Rapport de mélange de la vapeur d'eau, QV
-  Température du point de rosée, TD
-  Écart du point de rosée, ES
-  Humidité relative, HR
   ***Note:*** : Assurez-vous de fournir à ce plugin les dépendances
   ci-haut mentionnées ou alors, les résultats des
   plugins appelés par celui-ci (Voir la section "Ce plugin utilise").
   Pour plus de détails sur cet usage
   alternatif, voir la page de
   `documentation. <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__

\*Résultat(s):\*

-  Température du thermomètre mouillé, TTW (deg C)

| \*Algorithme:\*

-  `Algorithme pour TemperatureWetBulb - actuellement en
   Anglais <https://wiki.cmc.ec.gc.ca/images/7/7e/Spooki_-_Algorithm_TemperatureWetBulb.doc>`__

\*Références:\*

-  [[http://www.google.ca/url?sa=t&rct=j&q\ =&esrc=s&source=web&cd=1&ved=0CDYQFjAA&url=http%3A%2F%2Fwww.dmi.dk%2Fdmi%2Fsr03-16.pdf&ei=r-RRUYXyOYbf0QGszIHICA&usg=AFQjCNH7ibBkO9n3F0UNPian\ :sub:`Ve`-flf8WQ&bvm=bv.44342787,d.dmQ&cad=rja][Nielsen,
   N. W. and Petersen, C., 2003: A Generalized Thunderstorm Index
   Developed for DMI\ :sub:`HIRLAM`. Danish Meteorological Institute
   Scientific Report 03-16, 27 pp.]]
-  Bluestein, H. B., 1992: Synoptic-Dynamic Meteorology in Midlatitudes
   Volume 1: Principles of Kinematics and Dynamics. Oxford Univeristy
   Press, 431 pp.
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0493%281980%29108%3C1046%3ATCOEPT%3E2.0.CO%3B2][Bolton,
   D. 1980: The computation of equivalent potential temperature. Mon.
   Wea. Rev., 108, 1046-1053.]]
-  `Brunet, N., 2001: Les Fonctions Thermodynamiques et le Fichier de
   Constantes <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology in
   Midlatitudes. Wiley-Blackwell, 407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.

\*Mots clés:\*

-  MÉTÉO/WEATHER, température/temperature, thermomètremouillé/wet-bulb,
   humidité/humidity

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureWetBulb/testsFiles/inputFile.std] >>
                [TemperatureWetBulb] >>
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

 
