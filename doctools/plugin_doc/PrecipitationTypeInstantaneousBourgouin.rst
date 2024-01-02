===============================================
Spooki: PrecipitationTypeInstantaneousBourgouin
===============================================

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

`PrecipitationTypeInstantaneousBourgouin <classPrecipitationTypeInstantaneousBourgouin.html>`__

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

`Francais <../../spooki_french_doc/html/pluginPrecipitationTypeInstantaneousBourgouin.html>`__

**Description:**

-  Calculation of the type of instantaneous precipitation by using the
   Bourgouin method, based on the available energy in the cold and warm
   layers in altitude. More specifically, this method examines the
   temperature profile and takes into account the positive and negative
   energies with respect to the 0 deg C isotherm to decide the type of
   precipitation according to the energetic reference values. The
   positive energy (negative) is defined here as the area on a tephigram
   where the temperature is positive (negative, respectively).
-  The energy layers, obtained by the mean isotherm method
   (`EnergyMeanIsothermMethod <classEnergyMeanIsothermMethod.html>`__
   plug-in), are delimited by the freezing levels (in pressure) produced
   by the `FreezingLevel <classFreezingLevel.html>`__ plug-in.

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  Air temperature, TT
-  Total precipitation rate, RT
   ***Note:*** Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results called by this plug-in (see
   the section "this plug-in uses"). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

**Result(s):**

-  Type of instantaneous precipitation, T6 (2D, no units). Coded value
   from 1 to 6 such as :
   1: rain
   2: mixed rain/snow
   3: freezing rain
   4: ice pellets
   5: snow
   6: insufficient precipitation rate (less than 0.2mm/h)

**Algorithm:**

-  https://wiki.cmc.ec.gc.ca/w/images/f/f2/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.doc
-  https://wiki.cmc.ec.gc.ca/w/images/4/4b/Spooki_-_Algorithme_PrecipitationTypeInstantaneousBourgouin.pdf

**Reference:**

-  Reference article on the Bourgouin method :
   https://wiki.cmc.ec.gc.ca/w/images/5/59/Spooki_-_Article_ref_Bourgouin.pdf
-  Inspired from the operational program ''gembrgouin''

**Keywords:**

-  MÉTÉO/WEATHER, énergie/energy, aire/area, isotherme/isotherm,
   méthode/method , téphigramme/tephigram

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/PrecipitationTypeInstantaneousBourgouin/testsFiles/inputFile.std] >>
                    ( [Copy] + [FreezingLevel --outputVerticalRepresentation PRESSURE --maxNbFzLvl 10 ]  ) >>
                    [PrecipitationTypeInstantaneousBourgouin] >>
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
`PrecipitationTypeInstantaneousBourgouin <classPrecipitationTypeInstantaneousBourgouin.html>`__
:sup:``[code] <PrecipitationTypeInstantaneousBourgouin_8cpp_source.html>`__`

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
