================================
Spooki: SpatialWeightedAveraging
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

`SpatialWeightedAveraging <classSpatialWeightedAveraging.html>`__

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

`Français <../../spooki_french_doc/html/pluginSpatialWeightedAveraging.html>`__

**Description:**

-  It is a 2-D spatial weighted averaging based on a specific kernel
-  The kernel can take on the shape of different functions, such as a
   Gaussian
-  In the specific case where it is applied to a binary field (0 ou 1),
   the result can be interpreted as a PDF

**Iteration method:**

-  Point-by-point

**Dependencies:**

-  One or many gridded fields
-  ME field (only at one given time forecast) when the option
   "--altDiffMax" is used
-  MG field (only at one given time forecast) when the option
   "--landFracDiffMax" is used
-  SLX field (the same time forecasts of the X field) when the option
   "--slopeIndexDiffMax" is used

**Result(s):**

-  A weighted average based on a specific kernel

**Algorithm:**

.. code-block:: text

           For each point of the grid, we calculate the average from a set of grid points defined by a search radius.
           This average can be weighted according to a Gaussian or be uniform. In the case of a grid with limited area,
           the calculation of the average at the grid points near the borders is calculated with a sample of points more
           restricted than elsewhere on the grid. If the user prefers to exclude these points, since the search radius cannot
           be fully respected, the --excludeEdges option must be used and these grid points will be set to -999.

           This algorithm also makes it possible to restrict our sample of points to certain specific conditions such as the
           topography, land-to-water ratio, a slope index and a certain range of values.

           ---------------------------------------
           Definition of the important variables
           ---------------------------------------

           For r,            the search radius
           For d,            the distance between a grid point and the central grid point being treated 
           For h,            the smoothing parameter 
           For distanceType, either POINTS or KM
           For Smax,         the summation of the weights
           For Sum,          the summation of the weighted values 
           For Moy,          the average

           For altDiffMax,         maximum threshold in absolute value of the altitude (ME) difference between the processed grid point and those used to calculate the average.
           For landFracDiffMax,    maximum threshold in absolute value of the land-fraction (MG) difference between the processed grid point and those used to calculate the average.
           For slopeIndexDiffMax,  maximum threshold in absolute value of the slope index (SLX) difference between the processed grid point and those used to calculate the average.
           For minValue,           minimum value for a grid point to be selected in the average calculation. (ex: if minValue = 3, the average will be calculated only with the points > 3)
           For maxValue,           maximum value for a grid point to be selected in the average calculation. (ex: if maxValue = 10, the average will be calculated only with the points < 10)

           diff_me_abs  = |ME(i,j)  - ME(i+a,j+b) |
           diff_mg_abs  = |MG(i,j)  - MG(i+a,j+b) |
           diff_slx_abs = |SLX(i,j) - SLX(i+a,j+b)|

           ----------------------------------
           Definition of the 2 kernel types
           ----------------------------------
           If --kernelType GAUSSIAN
               kernel(d,h) = exp((-0.5*(d^2))/h^2)

           If --kernelType UNIFORM
               kernel(d,h) = 1

           Average calculation for all grid points when possible

           If distanceType = POINTS
              The distance d between the central grid point and those around is calculated with the equation of Pythagoras
           else if distanceType = KM
              The ezCalcDist function is used


           Loop over each grid point

           If the --excludeEdges option is used
               Make sure that the distance between this point and the border of the grid is <= r
           Otherwise
               point = -999

           Smax = 0
           Sum  = 0

           ---------------------------------------------------------------------------------------------------------------------------------------------------------
           We calculate the maximum value of the summation for the points inside the search radius, with an altitude difference (ME) in absolute value <= altDiffMax,
           with a difference in fraction of the land (MG) in absolute value <= landFracDiffMax, with a difference in slope index (SLX) in absolute value <= slopeIndexDiffMax, 
           with a value > minValue and finally with a value < maxValue
           ---------------------------------------------------------------------------------------------------------------------------------------------------------
           If d <= r &&  diff_me_abs <= altDiffMax && diff_mg_abs <= landFracDiffMax && diff_slx_abs <= slopeIndexDiffMax && valeur(X) > minValue & valeur(X) < maxValue
               Smax = Smax + kernel(d,h,kernelType)
               Sum  = Sum + kernel(d,h,kernelType)*value(of the grid point)

           Once all the points within the search radius are counted, the average is normalized:
           Moy = Sum/Smax

**Reference:**

-  `Description of the KDE
   method <http://fr.wikipedia.org/wiki/Kernel_density_estimation>`__
-  `Description of the Gaussian
   function <http://fr.wikipedia.org/wiki/Gaussian_function>`__
-  `Doc on the Forecasting Thunderstorm project at
   ECCC <https://wiki.cmc.ec.gc.ca/wiki/File:Forecasting_thunderstorms.pptx>`__
-  `Doc on the KDE project at
   ECCC <https://wiki.cmc.ec.gc.ca/wiki/File:HRDPS_EarlyResults2015_v2.pptx>`__

**Keywords:**

-  UTILITAIRE/UTILITY, statistique/statistics, noyau/kernel, estimation,
   probabilité/probability, gaussienne/gaussian, pdf, lissage/smoothing,
   normal, distribution

**Usage:**

**Call example:** ````

::

       ...
       spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/SpatialWeightedAveraging/testsFiles/inputFile.std] >>
                   [SpatialWeightedAveraging --searchRadius 15 --kernelType GAUSSIAN --distanceType KM --smoothingParameter 5] >>
                   [WriterStd --output /tmp/$USER/outputFile.std]"
       ...
       

**Results validation:**

**Contacts:**

-  Authors : `Marc
   Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__, `Daniel
   Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__
-  Coded by : `Louise
   Faust <https://wiki.cmc.ec.gc.ca/wiki/Louise_Faust>`__, `Sébastien
   Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__, `Guylaine
   Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to
`SpatialWeightedAveraging <classSpatialWeightedAveraging.html>`__
:sup:``[code] <SpatialWeightedAveraging_8cpp_source.html>`__`

Unit tests

`Evaluation tree <SpatialWeightedAveraging_graph.png>`__

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
