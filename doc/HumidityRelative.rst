HumidityRelative
================

Français
--------

Description:
~~~~~~~~~~~~

Calcul de l'humidité relative, rapport entre la pression partielle de la
vapeur d'eau contenue dans l'air et la pression de vapeur saturante à la
même température.

Méthode d'itération:
~~~~~~~~~~~~~~~~~~~~

Point par point

Dépendances:
~~~~~~~~~~~~

Température de l'air, TT et un des champs suivants:

Humidité spécifique, HU

Rapport de mélange de la vapeur d'eau, QV

Température du point de rosée, TD / Écart du point de rosée, ES

Résultat(s):

Humidité relative, HR (fraction)

Algorithme:

-Si la clé ,RPN=n'est pas activée:

Soit TT la température de l'air (deg C): Calcul de la pression de vapeur
saturante, SVP (hPa) avec le plugin SaturationVapourPressure. /Si les
champs d'entrée sont l'humidité spécifique, HU (kg/kg) ou le rapport de
mélange de la vapeur d'eau, QV (kg/kg) ou la température du point de
rosée, TD (deg C) ou l'écart du point de rosée, ES (deg K ou deg C):
Calcul de la pression de vapeur, VPPR (hPa) avec le plugin
VapourPressure. HR = VPPR/SVP où HR est l'humidité relative en fraction.
-Si la clé ,RPN=est activée: /Si les champs d'entrée sont l'humidité
spécifique, HU (kg/kg) et la température de l'air (deg K): Calcul de la
pression, PX (Pa) avec le plugin Pressure. Appel de la fonction
shuahr.ftn90 pour obtenir l'humidité relative, HR (fraction). /Si les
champs d'entrée sont la rapport de mélange de la vapeur d'eau, QV
(kg/kg) et température de l'air, TT (deg K): Calcul de l'humidité
spécifique, HU (kg/kg) avec le plugin HumiditySpecific. Calcul de la
pression, PX (Pa) avec le plugin Pressure. Appel de la fonction
shuahr.ftn90 pour obtenir l'humidité relative, HR (fraction)./Si les
champs d'entrée sont la température du point de rosée, TD (deg K) ou
l'écart du point de rosée, ES (deg K ou deg C) et la température de
l'air (deg K): Calcul de l'écart du point de rosée, ES (deg K ou deg C)
avec le plugin DewPointDepression si nécessaire. Calcul de la pression,
PX (Pa) avec le plugin Pressure. Appel de la fonction sesahr.ftn90 pour
obtenir l'humidité relative, HR (fraction). Notes: Lorsque plusieurs
champs des dépendances et le champ TT sont disponibles en entrée, le
calcul sera effectué avec le champ qui a le plus de niveaux en commun
avec TT dans l'ordre de préférence (en cas d'égalité) avec HU suivi de
QV, et finalement ES/TD. Lorsque la clé ,RPN=est activée et l'attribut
de ,iceWaterPhase=est BOTH, ,temperaturePhaseSwitch=n'est pas accepté et
273.16K (le point triple de l'eau) est attribué aux fonctions
sesahr.ftn90 et shuahr.ftn90.

Références:
~~~~~~~~~~~

`Librairie thermodynamique de
RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
[[http://fr.wikipedia.org/wiki/Humidit%C3%A9_relative%22%20target=%22_blank][Wikipedia
: Humidité relative]]

Mots clés:
~~~~~~~~~~

MÉTÉO/WEATHER, température/temperature, humidité/humidity

Usage:
~~~~~~

Exemple d'appel: python3 import fstpy.all as fstpy import spookipy.all
as spooki records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
"/pluginsRelatedStuff/HumidityRelative/testsFiles/inputFile.std").to:sub:`pandas`\ ()
records=HumidityRelative(records ,iceWaterPhase=BOTH
,temperaturePhaseSwitch=-40C)()
fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) :`Daniel Figueras <file:///wiki/Daniel_Figueras>`__ Codé par :
`Jonathan St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__,
`Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__ Ce plugin est utilisé
par:

English
-------

Description:
~~~~~~~~~~~~

Calculation of the relative humidity, the ratio between the partial
pressure of water vapour content in the air and the saturated vapour
pressure at the same temperature.

Iteration method:
~~~~~~~~~~~~~~~~~

Point-by-point

Dependencies:
~~~~~~~~~~~~~

Air temperature, TT and one of the following fields:

Specific humidity, HU

Water vapour mixing ratio, QV

Dew point temperature, TD / Dew point depression, ES

Result(s):

Relative humidity, HR (fraction)

Algorithm:

-If the ,RPN=key is NOT activated:

For the ambient temperature, TT (deg C): Calculation of the saturation
vapour pressure, SVP (hPa) with the SaturationVapourPressure plug-in /If
the input field is the specific humidity, HU (kg/kg) or the water vapour
mixing ratio, QV (kg/kg) or the dew point temperature, TD (deg C) or the
dew point depression, ES (deg K or deg C): Calculation of the vapour
pressure, VPPR (hPa) with the VapourPressure plug-in HR = VPPR/SVP where
HR is the relative humidity in fraction -If the ,RPN=key is activated:
/If the input fields are the specific humidity, HU (kg/kg) and the air
temperature, TT (deg K) Calculate the pressure, PX (Pa) with the
Pressure plug-in Call the function shuahr.ftn90 to obtain the relative
humidity, HR (fraction) /If the input fields are the water vapour mixing
ratio, QV (kg/kg) and the air temperature, TT (deg K) Calculate the
specific humidity, HU (kg/kg) with the HumiditySpecific plug-in
Calculate the pressure, PX (Pa) with the Pressure plug-in Call the
function shuahr.ftn90 to obtain the relative humidity, HR (fraction)/If
the input fields are the dew point temperature, TD (deg K) or the dew
point depression, ES (deg K or deg C) and the air temperature, TT (deg
K): Calculate the dew point depression, ES (deg K or deg C) with the
DewPointDepression plug-in if necessary Calculate the pressure, PX (Pa)
with the Pressure plug-in Call the function sesahr.ftn90 to obtain the
relative humidity, HR (fraction) Note: When several fields of the
dependencies and TT are available in the input, the calculation will be
done with the field that has the most number of levels in common with
TT, in order of preference (in case of equality) with HU followed by QV
and finally ES/TD. When the ,RPN=key is activate and the attribut to
,iceWaterPhase=is BOTH, ,temperaturePhaseSwitch=is no accepted and
273.16K (the triple point of water) is assigned to the sesahr.ftn90 and
shuahr.ftn90 functions.

Reference:
~~~~~~~~~~

`RPN thermodynamic
library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
[[http://en.wikipedia.org/wiki/Relative_humidity%22%20target=%22_blank][Wikipedia
: relative humidity]]

Keywords:
~~~~~~~~~

MÉTÉO/WEATHER, température/temperature, humidité/humidity

Usage:
~~~~~~

#. Call example:

   python3 import fstpy.all as fstpy import spookipy.all as spooki
   records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
   "/pluginsRelatedStuff/HumidityRelative/testsFiles/inputFile.std").to:sub:`pandas`\ ()
   records=HumidityRelative(records ,iceWaterPhase=BOTH
   ,temperaturePhaseSwitch=-40C)()
   fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Contacts:
~~~~~~~~~

Author :`Daniel Figueras <file:///wiki/Daniel_Figueras>`__ Coded by :
`Jonathan St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__,
`Guylaine Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
