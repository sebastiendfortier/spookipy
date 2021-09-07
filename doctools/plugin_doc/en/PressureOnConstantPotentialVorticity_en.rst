English
-------

**Description:**

-  Find the atmospheric pressure for a surface of constant Ertel
   potential vorticity (PV).

\*Iteration method:\*

-  Column by column from the top of the atmosphere

\*Dependencies:\*

-  Wind component along the X-axis of the grid, UU

-  Wind component along the Y-axis of the grid, VV

-  Air temperature, TT

   | ***Note:*** : Be sure to provide the dependencies mentioned above
     to this plug-in or the results of
   | the plug-ins called by this plug-in (See the "this plug-in uses"
     section). For more details on this
   | alternative use, see the
     `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/Documentation/Description_g%C3%A9n%C3%A9rale_du_syst%C3%A8me#RefDependances>`__
     page.

\*Result(s):\*

-  Pressure on a surface of constant potential vorticity, PPVU (hPa)

\*Algorithm:\*

.. code:: example

    For PV (1/s),     the potential vorticity of Ertel.
    For PX (hPa),     the model pressure.
    For TH (K),       the potential temperature.
    For ThetaMax (K), the maximum potential temperature.
    For PXTH (hPa),   the pressure of ThetaMax.
    For PPVU (hPa),   the pressure of the surface of constant potential vorticity.
    For CoriolisSign, the sign of the Coriolis parameter according to the northern or southern hemisphere.
    Soit PVU,         the desired PVU values.

    ThetaMax = 380K
    Initialize to -1 all points in PPVU matrix

    Loop on the columns of the matrix (i * j):
       Loop on the desired PVU values (p):
            Loop on the column levels (k), skipping the first and last levels:    
                If ( TH(k) <= ThetaMax )
                    Calculate PXTH (see formula below)
                End if

                If (CoriolisSign * PV(k) <= PVU(p))
                    Calculate PPVU (see formula below)
                End if    
            End of loop on column levels (k)

            If ( PPVU(p) = -1 )
                PPVU(p) = PXTH
            End if
        End of loop on PVU values (p)
    End of loop on columns

    Calculate PXTH:
          If ( abs (TH(k) - TH(k -1) < epsilon (10e-5) )
                 :math:`\mathrm{ PXTH = PX_{k}}`
         Else
              :math:`\mathrm{ AAA = 1 / ( TH_{k} - TH_{k -1} )}`
             
    :math:`\mathrm{ PXTH = AAA * ( PX_{k} * ( ThetaMax - TH_{k - 1} )
    + PX_{k -1} * ( TH_{k} - ThetaMax ) )}`
         End if

    Calculate PPVU:
       If ( CoriolisSign \* ( PV(k) - PV(k - 1) ) >= 0 )
              :math:`\mathrm{ PPVU_{p} = PX_{k}}`
       Else
              :math:`\mathrm{ AAA = 1 / ( PV_{k} - PV_{k - 1} )}`
             
    :math:`\mathrm{ WEIGHT = AAA * ( CoriolisSign * PVU_{p} - PV_{k -
    1} )}`
             
    :math:`\mathrm{ WEIGHTMINUS = AAA * ( PV_{k} - CoriolisSign *
    PVU_{p} )}`
              :math:`\mathrm{ PPVU_{p} = PX_{k} * WEIGHT + PX_{k - 1} *
    WEIGHTMINUS}`
       End if
       If ( PPVU(p) < PXTH )
              :math:`\mathrm{ PPVU_{p} = PXTH}`
       End if

**Reference:**

-  Code Fortran d'André Plante pressure\ :sub:`onpvsurface`.F90 et
   mod\ :sub:`pv`.F90, git clone
   `git@g.nosp@m.itla.nosp@m.b.sci.nosp@m.ence.nosp@m..gc.c.nosp@m.a <#>`__:cmdn:sub:`utils`/utilitaires.git

\*Keywords:\*

-  MÉTÉO/WEATHER, PVU, tourbillon potentiel/potential vorticity,
   tropopause dynamique/dynamic tropopause, température
   potentielle/potential temperature

\*Usage:\*

**Call example:**

.. code:: example

    ...
    spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PressureOnConstantPotentialVorticity/testsFiles/inputFile.std] >>
                [PressureOnConstantPotentialVorticity --PVU 2.0] >>
                [WriterStd --output /tmp/$USER/outputFile.std]"
    ...

**Results validation:**

**Contacts:**

-  Author : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Coded by : `Simon
   Prud'Homme <https://wiki.cmc.ec.gc.ca/wiki/User:Prudhommes>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to

Unit tests

| **Uses:**
| **Used by:**

 
