Français
--------

Description:
~~~~~~~~~~~~

Calcul de l'humidex. L'humidex est un indice qui vise à quantifier
l'inconfort créé par une combinaison de la chaleur et de l'humidité.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Température de l'air en surface (TTC) . et un des champs suivants à la
surface: Humidité spécifique, HU Humidité relative, HR Rapport du
mélange de la vapeur d'eau, QV Température de point de rosée, TD Écart
du point de rosée, ES

Résultat(s):
~~~~~~~~~~~~

Indice humidex, HMX (scalaire, sans unité)

Algorithme:
~~~~~~~~~~~

Soit TTC la température de l'air à la surface records=deg(records C)()

#. Calculer TD avec le plugin TemperatureDewPoint.
#. Soit es(TD), la pression partielle de la vapeur [Pa] à saturation.
   Celle-ci peut être calculée avec le plugin SaturationVapourPressure
   en utilisant TD au lieux de TTC avec l'option ,iceWaterPhase=WATER

On calcule ensuite l'humidex: HMX = TTC + (0.5555) \* (es(TD)10) Si
HMXTTC resultat = HMX Sinon resultat = TTC

Références:
~~~~~~~~~~~

`Description of the humidex by
ECCC <http://ec.gc.ca/meteo-weather/default.asp?lang=En&amp;n=6C5D4990-1#humidex%22%20class=%22external%20text%22%20rel=%22nofollow>`__
`Scribe
specifications <https://wiki.cmc.ec.gc.ca/images/0/0d/SITS14_specs.pdf%22%20class=%22external%20text%22%20rel=%22nofollow>`__

Mots clés:
~~~~~~~~~~

MÉTÉO/WEATHER, température/temperature, Humidité/humidité

Usage:
~~~~~~

#. Exemple d'appel:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std").to_pandas()
       s=Humidex(records).compute()
       fstpy.StandardFileWriter("/tmp/"+USER+"/outputFile.std",records).to_fst()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) : `Agnieszka
Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__

Codé par : `Philippe
Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

English
-------

Description:
~~~~~~~~~~~~

Humidex calculation. The humidex index aims to quantify the discomfort
caused by a combination of heat and humidity.

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

Air surface temperature, TTC and one of the following fields at the
surface: Specific humidity, HU Relative humidity, HR Water vapour mixing
ratio, QV Dew point temperature, TD Dew point depression, ES

Result(s):
~~~~~~~~~~

Humidex index, HMX (scalar, unitless)

Algorithm:
~~~~~~~~~~

TTC is the Temperature records=Celsius(records Degrees)() Calculate TD
with the TemperatureDewPoint plugin. ES(TT) is the Saturation Vapour
Pressure. This value can be obtained with the SaturationVapourPressure
plugin by using TD instead of TTC with the option ,iceWaterPhase=WATER
We calculate the Humidex: HMX = TTC + (0.5555) \* (ES(TT)10) if HMXTTC
result = HMX else result = TTC

Reference:
~~~~~~~~~~

-  `Description of the humidex by
   ECCC <http://ec.gc.ca/meteo-weather/default.asp?lang=En&amp;n=6C5D4990-1#humidex%22%20class=%22external%20text%22%20rel=%22nofollow>`__
-  `Scribe
   specifications <https://wiki.cmc.ec.gc.ca/images/0/0d/SITS14_specs.pdf%22%20class=%22external%20text%22%20rel=%22nofollow>`__

Keywords:
~~~~~~~~~

MÉTÉO/WEATHER, température/temperature, humidité/humidity

Usage:

#. Call example:

   .. code:: python

       python3
       import fstpy.all as fstpy
       import spookipy.all as spooki
       records=fstpy.StandardFileReader(SPOOKI_DIR + "/pluginsRelatedStuff/Humidex/testsFiles/inputFile.std").to_pandas()
       records=spooki.Humidex(records).compute()
       fstpy.StandardFileWriter("/tmp/"+USER+"/outputFile.std",records).to_fst()

Contacts:
~~~~~~~~~

Author : `Agnieszka
Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__

Coded by : `Philippe
Lachapelle <https://wiki.cmc.ec.gc.ca/wiki/User:lachapellep>`__

Support :

-  `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
-  `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
