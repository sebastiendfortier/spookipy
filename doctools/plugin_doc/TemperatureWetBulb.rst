==========================
Spooki: TemperatureWetBulb
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

`TemperatureWetBulb <classTemperatureWetBulb.html>`__

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

`Francais <../../spooki_french_doc/html/pluginTemperatureWetBulb.html>`__

**Description:**

-  Calculates wet-bulb temperature, the temperature an air parcel would
   reach having a given potential temperature and water vapour content,
   if its liquid water content is evaporated until saturation while
   keeping a constant pressure.
   ***Note:*** If the pressure is smaller than 5hPa the calculation is
   not performed and TTW is set to -999.

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  Air temperature, TT
   **and** one of the following fields :
-  Specific humidity, HU
-  Water vapour mixing ratio, QV
-  Dew point temperature, TD
-  Dew point depression, ES
-  Relative humidity, HR
   ***Note:*** : Make sure to provide the dependencies listed above to
   this plug-in or to the plug-in results called by this plug-in (see
   the section "this plug-in uses"). For more details on this
   alternative use, see the
   `documentation <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/General_system_description#How_does_it_work.3F>`__
   page.

**Result(s):**

-  Wet-bulb temperature, TTW (deg C)

| **Algorithm:**
| `TemperatureWetBulb
  algorithm <https://wiki.cmc.ec.gc.ca/images/7/7e/Spooki_-_Algorithm_TemperatureWetBulb.doc>`__

**Reference:**

-  `Nielsen, N. W. and Petersen, C., 2003: A Generalized Thunderstorm
   Index Developed for DMI\_HIRLAM. Danish Meteorological Institute
   Scientific Report 03-16, 27
   pp. <http://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0CDYQFjAA&url=http%3A%2F%2Fwww.dmi.dk%2Fdmi%2Fsr03-16.pdf&ei=r-RRUYXyOYbf0QGszIHICA&usg=AFQjCNH7ibBkO9n3F0UNPian_Ve-flf8WQ&bvm=bv.44342787,d.dmQ&cad=rja>`__
-  Bluestein, H. B., 1992: Synoptic-Dynamic Meteorology in Midlatitudes
   Volume 1: Principles of Kinematics and Dynamics. Oxford Univeristy
   Press, 431 pp.
-  `Bolton, D. 1980: The computation of equivalent potential
   temperature. Mon. Wea. Rev., 108,
   1046-1053. <http://journals.ametsoc.org/doi/pdf/10.1175/1520-0493%281980%29108%3C1046%3ATCOEPT%3E2.0.CO%3B2>`__
-  `Brunet, N., 2001: Les Fonctions Thermodynamiques et le Fichier de
   Constantes <https://wiki.cmc.ec.gc.ca/images/6/60/Tdpack2011.pdf>`__
-  Markowski, P. and Y. Richardson, 2010: Mesoscale Meteorology
   i//#define INPUTFIELDNAME\_HU "HU"n Midlatitudes. Wiley-Blackwell,
   407 pp.
-  Rogers, R. R. and M. K. Yau, 1989: A Short Course in Cloud Physics,
   3rd Ed. Butterworth Heinemann, 290 pp.

**Keywords:**

-  MÉTÉO/WEATHER, température/temperature, thermomètremouillé/wet-bulb,
   humidité/humidity

**Usage:**

**Call example:** ````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/TemperatureWetBulb/testsFiles/inputFile.std] >>
                    [TemperatureWetBulb] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

**Results validation:**

**Contacts:**

-  Author : Neil Taylor
-  Coded by : Jonathan Cameron
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `TemperatureWetBulb <classTemperatureWetBulb.html>`__
:sup:``[code] <TemperatureWetBulb_8cpp_source.html>`__`

Units tests

`Evaluation tree <TemperatureWetBulb_graph.png>`__

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
