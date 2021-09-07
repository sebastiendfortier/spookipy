English
-------

**Description:**

-  Calculation of the dew point depression, a measure of atmospheric
   humidity
-  Difference between the temperature of an air parcel and the
   temperature at which the air of that parcel must be cooled, at
   constant pressure and humidity content, to attain saturation.

\*Iteration method:\*

-  Point-by-point

\*Dependencies:\*

-  Air temperature, TT

| \*and\* one of the following fields:

-  Dew point temperature, TD
-  Water vapour mixing ratio, QV
-  Specific humidity, HU

\*Result(s):\*

-  Dew point depression, ES (deg C)

\*Algorithm:\*

.. code:: example

    -If the --RPN key is NOT activated:

        *If the input fields are the specific humidity, HU (kg/kg) or
            the water vapour mixing ratio, QV (kg/kg) or
            the relative humidity, HR (fraction) and the air temperature, TT (deg C):

            Calculate the dew point temperature, TD (deg C) with the TemperatureDewPoint plug-in
            The dew point depression, ES (deg C or deg K) is calculated according to :
            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where TT or TD have the same units (deg C or deg K)

        *If the input fields are the dew point temperature, TD (deg C or deg K) and the air temperature, TT (deg C or deg K):

            The dew point depression, ES (deg C or deg K) is calculated according to :
            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where TT or TD have the same units (deg C or deg K)


    -If the --RPN key is activated:

        *If the input fields are the specific humidity, HU (kg/kg) and the air temperature, TT (deg K):

            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shuaes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the water vapour mixing ratio, QV (kg/kg) and the air temperature, TT (deg K):

            Calculate the specific humidity, HU (kg/kg) with the HumiditySpecific plug-in
            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shuaes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the relative humidity, HR (fraction) and the air temperature, TT (deg K):

            Calculate the pressure, PX (Pa) with the Pressure plug-in
            Call the function shraes.ftn90 to obtain the dew point depression, ES (deg C or deg K)

        *If the input fields are the dew point temperature, TD (deg C or deg K) and the air temperature, TT (deg C or deg K):

            ES = TT - TD  (if ES < 0.0 , ES = 0.0)
            where the dew point depression, ES is in deg C or deg K

    Notes:  When the input field is TD or HR, the phase change will presumably happen at the same time in the input field as in output field.
            When several fields of the dependencies and TT are available in the input, the calculation will be done with the field that has the most number of levels in common with TT, in order of preference (in case of equality) with HU followed by QV, HR and finally TD.
            When the --RPN key is activate and the attribut to --iceWaterPhase is BOTH, --temperaturePhaseSwitch is no accepted and 273.16K (the triple point of water) is assigned to the shuaes.ftn90 and shraes.ftn90 functions.
            With the --RPN key activated, the functions shuaes.ftn90 and shraes.ftn90 compare the dew point temperature with 273.16K (the triple point of water) to select if we calculate the dew point depression with respect to water or ice.
            Without the --RPN key, we compare the temperature with --temperaturePhaseSwitch to select if we calculate the dew point depression with respect to water or ice.

**Reference:**

-  `RPN thermodynamic
   library <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  `Wikipédia : dew point <http://en.wikipedia.org/wiki/Dew_point>`__
-  [[http://journals.ametsoc.org/doi/pdf/10.1175/1520-0450%281996%29035%3C0601%3AIMFAOS%3E2.0.CO%3B2][Alduchov,
   O. A., and R. E. Eskridge, 1996: Improved Magnus form approximation
   of saturation vapor pressure. ''J. Appl. Meteor.'', '''35''',
   601-609.]]

\*Keywords:\*

-  MÉTÉO/WEATHER, température/temperature, pointderosée/dewpoint,
   humidité/humidity

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/DewPointDepression/testsFiles/inputFile.std] >>
                [DewPointDepression --iceWaterPhase BOTH --temperaturePhaseSwitch -40C] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Daniel Figueras <file:///wiki/Daniel_Figueras>`__
-  Coded by : `Jonathan
   St-Cyr <https://wiki.cmc.ec.gc.ca/wiki/User:Stcyrj>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Units tests

| **Uses:**
| **Used by:**

 
