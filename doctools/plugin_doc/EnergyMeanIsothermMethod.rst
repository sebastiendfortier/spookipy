================================
Spooki: EnergyMeanIsothermMethod
================================

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

`EnergyMeanIsothermMethod <classEnergyMeanIsothermMethod.html>`__

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

`Français <../../spooki_french_doc/html/pluginEnergyMeanIsothermMethod.html>`__

**Description:**

-  Calculates the available energy in a column according to the "mean
   isotherm" method (see references). This method, initially developed
   using a tephigram, is based on the definition of energy and the
   calculation of area on a thermodynamic diagram. It can be
   demonstrated that the available energy in a layer is proportional to
   the mean temperature of the layer as well as the pressure at the base
   and top of the layer. The temperature fields considered (a field can
   be an isotherm) dictate whether the energy will be positive of
   negative.
   ***Note:*** This plug-in can be used: to calculate the energy of a
   lifted parcel, the energy of the environment with respect to an
   isotherm or between 2 tephigrams. Hence it is crucial to define the
   temperature field against which the comparison is done.
   ***Note2:*** This plug-in behaves slightly differently when called by
   the
   `LevelOfFreeConvectionAndEquilibrium <pluginLevelOfFreeConvectionAndEquilibrium.html>`__
   plug-in.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Temperature field (e.g. temperature of the lifted parcel for CAPE
   calculation, temperature of the environment for the precipitation
   types calculated according to the Bourgouin method, etc...)
-  Temperature field against which the comparison is done (can be
   constant, ex: isotherm 0 deg C)...
   ***Note:*** Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results called by this plug-in (see
   the section "this plug-in uses"). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

**Result(s):**

-  The plugin produces 2 3D fields, where the 3rd dimension is the
   number of layers delimited by the APX levels, height in pressure of
   the levels delimiting the positive and negative energy layers (ex:
   freezing levels, level of free convection, level of equilibrium;
   etc...): ...
   ENP, positive energy (J.Kg-1)
   ENN, negative energy (J.Kg-1)
   ***Note:*** Each layer contains either a positive energy (ENP) or a
   negative energy (ENN).

**Algorithm:**

-  https://wiki.cmc.ec.gc.ca/images/0/08/Spooki_-_Algorithme_EnergyMeanIsothermMethod.odt
-  https://wiki.cmc.ec.gc.ca/images/a/af/Spooki_-_Algorithme_EnergyMeanIsothermMethod.pdf

**References:**

-  "Atmospheric Thermodynamics", Iribarne, J.V., and Godson, W.L.
   (Riedel, 2nd edition, 1981)

**Keywords:**

-  MÉTÉO/WEATHER, énergie/energy, aire/area, isotherme/isotherm,
   méthode/method , téphigramme/tephigram

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/EnergyMeanIsothermMethod/testsFiles/inputFile.std] >>
                    ([Copy] + ([Select --fieldName TT] >> [SetConstantValue --value 0] >> [Zap --fieldName CF]) +
                     [Pressure --coordinateType AUTODETECT --referenceField TT] ) >>
                    ( [Copy] + [VerticalScan --referenceField TT --comparisonValueOrField 0 --comparisonType CONSTANTVALUE --maxNbOccurrence 5 --consecutiveEvents INF --outputVerticalRepresentation PRESSURE --epsilon 1e-04]  ) >>
                    [EnergyMeanIsothermMethod --temperature TT --comparisonTemperature CF] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : `Sandrine
   Edouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`EnergyMeanIsothermMethod <classEnergyMeanIsothermMethod.html>`__
:sup:``[code] <EnergyMeanIsothermMethod_8cpp_source.html>`__`

Unit tests

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
