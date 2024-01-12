# -*- coding: utf-8 -*-
import os
import pkg_resources
from pathlib import Path

def _get_version():
   try:
       version = pkg_resources.resource_string('spookipy', 'VERSION').decode('utf-8').strip()
   except IOError:
       version = 'unknown'
   return version

__version__ = _get_version()

from .addelementsbypoint import *
from .addtoelement import *
from .applyunary import *
from .arithmeticmeanbypoint import *
from .cloudfractiondiagnostic import *
from .coriolisparameter import *
from .dewpointdepression import *
from .filterdigital import *
from .georgekindex import *
from .gridcut import *
from .gridpointdifference import *
from .gridpointdistance import *
from .helicity import *
from .humidex import *
from .humidityrelative import *
from .humidityrelativeweightedmean import *
from .humidityspecific import *
from .humidityutils import *
from .interpolationhorizontalgrid import *
from .interpolationhorizontalpoint import *
from .mask import *
from .matchlevelindextovalue import *
from .minmaxlevelindex import *
from .minmaxvertically import *
from .multiplyelementby import *
from .multiplyelementsbypoint import *
from .opelementsbycolumn import *
from .opelementsbyvalue import *
from .percentiletopercentage import *
from .plugin import *
from .precipitationamount import *
from .pressure import *
from .printdf import *
from .replacedataifcondition import *
from .saturationvapourpressure import *
from .science import *
from .setconstantvalue import *
from .setlowerboundary import *
from .setupperboundary import *
from .statisticsvertically import *
from .subtractelementsvertically import *
from .temperaturedewpoint import *
from .temperaturepotential import *
from .temperaturevirtual import *
from .thickness import *
from .timeintervaldifference import *
from .timeintervalminmax import *
from .totaltotalsindex import *
from .vapourpressure import *
from .watervapourmixingratio import *
from .windchill import *
from .winddirection import *
from .windmax import *
from .windmodulus import *
from .writerstd import *

from .configparsingutils import *
from .utils import *

