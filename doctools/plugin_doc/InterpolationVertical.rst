=============================
Spooki: InterpolationVertical
=============================

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

`InterpolationVertical <classInterpolationVertical.html>`__

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

`Francais <../../spooki_french_doc/html/pluginInterpolationVertical.html>`__

**Description:**

-  Vertical interpolation module developed from the EZINTERPV library of
   RMNLIB, which is based on an ensemble of classical 1D interpolation
   routines
-  Plug-in that processes all types of vertical levels (eta, sigma,
   hybrid, pressure, ...)
-  Possibility to interpolate directly in geometric height (meters) with
   respect to the mean sea level or with respect to the ground in mb
   above ground, without using the EZINTERPV library

**NOTE** : For the moment, only the interpolations in geometric height
with respect to the mean sea level or to a pressure level are available

**Iteration method:**

-  Column-by-column

**Dependencies:**

-  One or more column(s) of values to interpolate vertically
-  Geopotential height (GZ), in the case of interpolation in height
-  Surface pressure (P0), in the case of interpolation on pressure
   levels
-  Hydrostatic pressure (PX), if the key –verticalLevelType is
   MILLIBARS\_ABOVE\_LEVEL

**Result(s):**

-  One or more column(s) interpolated on vertical levels or wanted
   heights, with the same units as the source

**Algorithm:**

-  if the –verticalLevelType METER\_SEA\_LEVEL key or –verticalLevelType
   METER\_GROUND\_LEVEL key is used, then for each of the heights to be
   interpolated to :

   -  search for the two geopotential heights GZ (in meters) that is
      surrounding the designated height
   -  deduction of the level indices surrounding the height on which to
      interpolate
   -  linear interpolation of the source column on the designated height

else :

-  transform the input levels into parameter pressure levels (could also
   be done by the EZINTERPV library)
-  interpolate from pressure level to pressure level, by using the
   EZINTERPV library

**References:**

-  `Library EZINTERPV of
   RMNLIB <https://wiki.cmc.ec.gc.ca/wiki/RPN-SI/RpnLibrairies/RMNLIB/INTERP1D/Ez_interpv_f90>`__

**Keywords:**

-  INTERPOLATION, extrapolation, niveaux/levels, vertical, ezinterpv

**Usage:**

| ***Notes:***
| For the –outputGridDefinitionMethod key :

-  USER\_DEFINED: the target vertical grid is define with the paramteres
   given to the keys –verticalLevelType and –verticalLevel. Warning: The
   horizontal grid will be the same as the input fields
-  FIELD\_DEFINED: the target vertical grid is definde by the reference
   field identified in the paramter of the –fieldName key. The reference
   field must only be available on a single grid and only the input
   fields on the same horizontal grid as the reference field will be
   interpolated.

For the –verticalLevelType key :

-  METER\_SEA\_LEVEL: interpolation with respect to the mean sea level
-  METER\_GROUND\_LEVEL: interpolation with respect to the ground
-  MILLIBARS\_ABOVE\_LEVEL : interpolation in millibars above the
   reference level
-  MILLIBARS : interpolation in millibars

For the –interpolationType key :

-  NEAREST: attributes the source value, that has the nearest index, to
   the target value
-  LINEAR: weighted average of the two nearest 2 source values
-  CUBIC\_WITH\_DERIVS: uses the nearest 2 source values and their
   derivatives to obtain the best possible estimation of the target
   value in function of its 3rd order derivatives (cubic method)
-  CUBIC\_LAGRANGE: 4th order interpolation method that uses the cubic
   splines (continuous function formed of cubic Lagrange polynomials).
   Requires the 4 nearest source values

For the –extrapolationType key :

-  NEAREST: the target value to extrapolate outside of the column is
   replaced by the nearest value of the source column
-  FIXED: the target values to extrapolate are replaced by a given
   numeric value (float specified by the keys –valueAbove and
   –valueBelow)
-  LAPSERATE: use the slope (specified by the keys –valueAbove and
   –valueBelow) between the target value and the nearest source value to
   determine the value to extrapolate

````

::

        ...
        spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/InterpolationVertical/testsFiles/inputFile.std] >>
                    [InterpolationVertical  -m USER_DEFINED --verticalLevel 1000,2000,3000,4000,6000 --verticalLevelType METER_SEA_LEVEL
                                            --interpolationType LINEAR --extrapolationType FIXED --valueAbove 999.0 --valueBelow 999.0] >>
                    [WriterStd --output /tmp/$USER/outputFile.std]"
        ...

-  `Other
   examples <https://wiki.cmc.ec.gc.ca/wiki/Spooki/en/Documentation/Examples#Example_of_vertical_interpolation>`__

| ***Notes:***
| For the interpolations towards levels in meters or millibars above
  level, only the LINEAR and NEAREST interpolations are supported. The
  SURFACE and SURFACE\_WIND extrapolations are not activated. If you
  deem these extrapolations necessary, please contact the SPOOKI team.
  Moreover, the interpolations from levels in meters or millibars above
  level are not surpported.

**Results validation:**

**Contacts:**

-  Author : `Sandrine
   Édouard <https://wiki.cmc.ec.gc.ca/wiki/User:Edouards>`__
-  Coded by : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Reference to `InterpolationVertical <classInterpolationVertical.html>`__
:sup:``[code] <InterpolationVertical_8cpp_source.html>`__`

Units tests

`Evaluation tree <InterpolationVertical_graph.png>`__

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
