Français
--------

Description :
~~~~~~~~~~~~~

Calcul de la pression de vapeur saturante en fonction de la température.

Méthode d'itération :
~~~~~~~~~~~~~~~~~~~~~

Point par Point

Dépendances :
~~~~~~~~~~~~~

Température de l'air (TT)

Résultat(s) :
~~~~~~~~~~~~~

Pression de vapeur saturante, SVP (hPa)

Algorithme :
~~~~~~~~~~~~

-Si la clé ,RPN=n'est pas activée:

Soit TT, la température de l'air (deg C)

Soit TPL, la température à laquelle il faut changer de la saturation par
rapport à l'eau liquide à la saturation par rapport à la glace (deg C)

Soit SVP, la pression de vapeur saturante (hPa)

Si TTTPL ou ,iceWaterPhase=WATER

SVP = AEw1\*EXP[AEw2\*TT/(AEw3 + TT)]

Sinon

SVP = AEi1\*EXP[AEi2\*TT/(AEi3 + TT)]

où selon Alduchov et Eskridge (1996)

AEw1=6.1094 AEi1=6.1121

AEw2=17.625 AEi2=22.587

AEw3=243.04 AEi3=273.86

-Si la clé ,RPN=est activée:

Soit TT, la température (degK)

Soit TPL, la température sous laquelle on calcule la pression de vapeur
saturante par rapport à la glace (degK)

Si TTTPL ou ,iceWaterPhase=WATER

Appeler la fonction sfoewa.ftn90 pour obtenir la pression de vapeur
saturante, SVP (Pa).

Sinon

Appeler la fonction sfoew.ftn90 pour obtenir la pression de vapeur
saturante, SVP (Pa).

Convertir SVP (Pa) en hPa:

SVP(hPa)=SVP(Pa)/100.0

Références :

`Alduchov, O. A., and R. E. Eskridge, 1996: Improved Magnus form
approximation of saturation vapor pressure. ''J. Appl. Meteor.'',
'''35''',
601-609 <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__

`Analyse de la pression de vapeur
saturante <https://wiki.cmc.ec.gc.ca/wiki/RPT/Analyse_de_la_pression_de_vapeur_saturante>`__

`Librairie thermodynamique de
RPN <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

Mots clés :

MÉTÉO/WEATHER, humidité/humidity, pression/pressure, saturation

Usage:

Exemple d'appel: python3 import fstpy.all as fstpy import spookipy.all
as spooki records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
"/pluginsRelatedStuff/SaturationVapourPressure/testsFiles/inputFile.std").to:sub:`pandas`\ ()
records=SaturationVapourPressure(records ,iceWaterPhase=BOTH
,temperaturePhaseSwitch=0.01C)()
fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Auteur(e) :Neil Taylor Codé par : `Guylaine
Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__ Ce plugin est utilisé
par:

English
-------

Description :
~~~~~~~~~~~~~

Calculates the saturation vapour pressure as a function of temperature.

Méthode d'itération :
~~~~~~~~~~~~~~~~~~~~~

Point-by-point

Dépendances :
~~~~~~~~~~~~~

Air temperature, TT

Résultat(s) :
~~~~~~~~~~~~~

Saturation vapour pressure, SVP (hPa)

Algorithme :
~~~~~~~~~~~~

-If the ,RPN=key is NOT activated:

For TT the air temperature (deg C)

For TPL the temperature at which to switch from saturation over water to
saturation over ice (deg C)

For SVP the saturation vapour pressure (hPa)

If TTTPL or ,iceWaterPhase=WATER

SVP = AEw1\*EXP[AEw2\*TT/(AEw3 + TT)]

else

SVP = AEi1\*EXP[AEi2\*TT/(AEi3+TT)]

where according to Alduchov and Eskridge (1996)

AEw1=6.1094 AEi1=6.1121

AEw2=17.625 AEi2=22.587

AEw3=243.04 AEi3=273.86

-If the ,RPN=key is activated:

For TT the temperature (deg K)

For TPL the temperature below which we calculate the saturation vapour
pressure with respect to ice (deg K)

If TTTPL or ,iceWaterPhase=WATER

Call rpn function sfoewa.ftn90 to obtain the saturation vapour pressure,
SVP (Pa)

else

Call rpn function sfoew.ftn90 to obtain the saturation vapour pressure,
SVP (Pa)

Convert SVP (Pa) to hPa:

SVP(hPa)=SVP(Pa)/100.0

Références :

`Alduchov, O. A., and R. E. Eskridge, 1996: Improved Magnus form
approximation of saturation vapor pressure. ''J. Appl. Meteor.'',
'''35''',
601-609 <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2>`__

`Analysis of saturation vapour
pressure <https://wiki.cmc.ec.gc.ca/wiki/RPT/en/Analysis_of_saturation_vapour_pressure>`__

`RPN thermodynamic
library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__

Mots clés :

MÉTÉO/WEATHER, humidité/humidity, pression/pressure, saturation

Usage:

Exemple d'appel: python3 import fstpy.all as fstpy import spookipy.all
as spooki records=fstpy.StandardFileReader(SPOOKI\ :sub:`DIR` +
"/pluginsRelatedStuff/SaturationVapourPressure/testsFiles/inputFile.std").to:sub:`pandas`\ ()
records=SaturationVapourPressure(records ,iceWaterPhase=BOTH
,temperaturePhaseSwitch=0.01C)()
fstpy.StandardFileWriter("*tmp*"[STRIKEOUT:USER]"/outputFile.std",records).to:sub:`fst`\ ()

Validation des résultats:
~~~~~~~~~~~~~~~~~~~~~~~~~

Contacts:
~~~~~~~~~

Author :Neil Taylor Coded by : `Guylaine
Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__

Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__
`CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__
