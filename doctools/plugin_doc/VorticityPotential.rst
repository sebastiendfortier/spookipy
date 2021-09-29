==========================
Spooki: VorticityPotential
==========================

.. raw:: html

   <div id="top">

.. raw:: html

   <div id="titlearea">

+--------------------------------------------------------------------------+
| .. raw:: html                                                            |
|                                                                          |
|    <div id="projectname">                                                |
|                                                                          |
| Spooki                                                                   |
|                                                                          |
| .. raw:: html                                                            |
|                                                                          |
|    </div>                                                                |
+--------------------------------------------------------------------------+

.. raw:: html

   </div>

.. raw:: html

   <div id="main-nav">

.. raw:: html

   </div>

.. raw:: html

   <div id="MSearchSelectWindow"
   onmouseover="return searchBox.OnSearchSelectShow()"
   onmouseout="return searchBox.OnSearchSelectHide()"
   onkeydown="return searchBox.OnSearchSelectKey(event)">

.. raw:: html

   </div>

.. raw:: html

   <div id="MSearchResultsWindow">

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="header">

.. raw:: html

   <div class="headertitle">

.. raw:: html

   <div class="title">

`VorticityPotential <classVorticityPotential.html>`__

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="contents">

.. raw:: html

   <div class="textblock">

`Français <../../spooki_french_doc/html/pluginVorticityPotential.html>`__

**Description:**

-  Calculation of Ertel's potential vorticity, PV.

**Iteration method:**

-  Column by column.

**Dependencies:**

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

**Result(s):**

-  Potential vorticity, PV (PVU units), 1 PVU = 1.e-6 K m^2 / ( kg s).

**Algorithm:**

.. code:: fragment

        For UU (m/s) and VV (m/s), respectively the wind components along the X-axis and Y-axis.
        For QQ (1/s),   the absolute vorticity.
        For PX (hPa),   the pressure of the model.
        For TT (K),     the air temperature.
        For TH (K),     the potential temperature.
        For CORP (1/s), the Coriolis parameter.
        
        Calculate the potential vorticity of Ertel, PV (in PVU units)

        grav     = 9.806160000000 (gravitational acceleration m s-2)
        ThetaMax = 380K

        Loop k on the levels :
            Loop on j :
                Loop on i :
                    If theta of the current point is larger than ThetaMax 
                        Set the PV to --PVU key value, but of the same sign as the Coriolis parameter
                    Else
                        Calculate PV (see formula below)
                        Convert the result in PVU units
                    End if
                End of loop on i
            End of loop on j
        End of loop on k

    PV calculation:
    The partial derivative of the log of theta according to PX must not
    be zero, because this quantity is used to divide by.
    It is limited to -1.e-7 (this quantity is negative)
    \\(\\mathrm{ DPX = ( ( PX\_{i,j,k+1} - PX\_{i,j,k-1} ) \* 100. )}\\)
    \\(\\mathrm{ DTH = ( TH\_{i,j,k+1} - TH\_{i,j,k-1} )}\\)
    \\(\\mathrm{ PV\_{i,j,k} = -grav \* ( QQ\_{i,j} - 1. / ( TT\_{i,j}
    \* min( -1.e-7, log( TH\_{i,j,k+1} / TH\_{i,j,k-1} ) / DPX ) ) \*
    }\\)
               \\(\\mathrm{ ( ( VV\_{i,j,k+1} - VV\_{i,jk-1} ) / DPX \*
    ( TT\_{i+1,j} - TT\_{i-1,j} ) / ( X\_{i+1,j} - X\_{i-1,j} ) - (
    UU\_{i,j,k+1} - UU\_{i,j,k-1} ) / DPX \* }\\)
               \\(\\mathrm{ ( TT\_{i,j+1} - TT\_{i,j-1} ) / ( Y\_{i,j+1}
    - Y\_{i,j-1} ) ) ) \* DTH / DPX }\\)

**Reference:**

-  Bluestein, H. B, 1992. Synoptic-Dynamic Meteorology in Midlatitudes,
   Volume I.
-  Code Fortran d'André Plante pressure\_on\_pv\_surface.F90 et
   mod\_pv.F90, git clone
   `git@g.nosp@m.itla.nosp@m.b.sci.nosp@m.ence.nosp@m..gc.c.nosp@m.a <#>`__:cmdn\_utils/utilitaires.git

**Keywords:**

-  MÉTÉO/WEATHER, vent/wind, tourbillon/vorticity, potentiel/potential

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/VorticityPotential/testsFiles/inputFile.std] >>
                    [VorticityPotential --maxPVU 2.0] >>
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

Reference to `VorticityPotential <classVorticityPotential.html>`__
:sup:``[code] <VorticityPotential_8cpp_source.html>`__`

Unit tests

`Evaluation tree <VorticityPotential_graph.png>`__

| **Uses:**

| **Used by:**

.. raw:: html

   </div>

.. raw:: html

   </div>

--------------

Generated by  |doxygen| 1.8.13

.. |doxygen| image:: doxygen.png
   :class: footer
   :target: http://www.doxygen.org/index.html
