English
-------

**Description:**

-  Calculation of the air density

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature, TT

-  | , PX
   | **and**, if the --virtualTemperature key is ACTUAL or BOTH, then
     one of the following fields at the surface is required:

-  Specific humidity, HU

-  Water vapour mixing ratio, QV

-  Dew point temperature, TD

-  Dew point depression, ES

-  Relative Humidity, HR

\*Result(s):\*

-  Air Density (Real, using the virtual temperature correction), M3
   (kg/m3)
-  Air Density (Dry), M3D (kg/m3)

\*Algorithm:\*

.. code:: example

    If the value of the --virtualTemperature key is DRY:
    1. Convert the temperature to Kelvin degrees, by adding 273.15, TTK
    2. Compute the air density using the following formula where RGASD equals 287.05 J kg-1 K-1:
         M3D = 100.0 * PX / (RGASD * TTK)

    If the value of the --virtualTemperature key is ACTUAL:
    1. Calculate VT using the TemperatureVirtual plug-in.
    2. Convert the virtual temperature to Kelvin degrees, by adding 273.15, VTK
    3. Compute the air density using the following formula where RGASD equals 287.05 J kg-1 K-1:
        M3 = 100.0 * PX / (RGASD * VTK)

    If the value of the --virtualTemperature key is BOTH:
        Calculate both variables M3 and M3D usgin the above formulae.

**Reference:**

`Wind energy project, air density
calculation <https://wiki.cmc.ec.gc.ca/wiki/Wind_energy_and_icing_forecasting_version3#Computing_M3_.28air_density_.7C_Densit.C3.A9_de_l.27air.29>`__

**Keywords:**

-  MÉTÉO/WEATHER, Densité de l'air/air density

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/AirDensity/testsFiles/inputFile.std] >>
                [AirDensity --virtualTemperature ACTUAL] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Agnes
   Barszcz <https://wiki.cmc.ec.gc.ca/wiki/Agn%C3%A8s_Barszcz>`__
-  Coded by : `Antoine
   Boisvert <https://wiki.cmc.ec.gc.ca/wiki/User:Boisvertan>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
