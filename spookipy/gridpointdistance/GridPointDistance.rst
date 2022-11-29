Description:
~~~~~~~~~~~~

-  Calculation of the distances on a horizontal grid between each point of which we know the latitude and longitude.
   The distance can be calculated in three different ways on each axis of the grid :
   -  centered distance : for one given point, angular distance between the previous point and the next point
   -  forward distance : for one given point, angular distance between the point and the next point
   -  backward distance : for one given point, angular distance between the point and the previous point

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  Grid of points (on at least one axis) of which we know the latitudes and longitudes respectively

Result(s):
~~~~~~~~~~

-  The distances GDX (X axis) and GDY (Y axis) between each point of the given grid (meters)

Algorithm:
~~~~~~~~~~

   For R, the mean radius of the Earth allowing to convert the angular distances GDX and GDY from radians to meters.
   For all the points i of latitude :math:`\lambda` (radians) and longitude :math:`\varphi` (radians), 
   we use, depending on the value of the "differenceType" key, the appropriate trigonometric formula to calculate the angular distances :

   If axis = X then  

       If differenceType = CENTERED then  

          :math:`GDX_{i} = R \cdot \arccos[\sin\lambda_{i-1} \cdot \sin \lambda_{i+1} + \cos\varphi_{i-1} \cdot \cos \varphi_{i+1} \cdot \cos(\varphi_{i+1} - \varphi_{i-1})]`  

          For the 1st level:  

          :math:`GDX_{i} = R \cdot \arccos[\sin\lambda_{i} \cdot \sin \lambda_{i+1} + \cos \varphi_{i}\cdot \cos \varphi_{i+1} \cdot \cos (\varphi_{i+1} -\varphi_{i})]`  

          For the last level:  

          :math:`GDX_{i} = R \cdot \arccos[\sin\lambda_{i} \cdot \sin \lambda_{i-1} + \cos \varphi_{i}\cdot \cos \varphi_{i-1} \cdot \cos (\varphi_{i} -\varphi_{i-1})]`  

      Else if differenceType = FORWARD then  

          :math:`GDX_{i} = R \cdot \arccos[\sin \lambda_{i} \cdot \sin \lambda_{i+1} + \cos \varphi_{i} \cdot \cos \varphi_{i+1} \cdot \cos (\varphi_{i+1} - \varphi_{i})]`  

          For the last level:  

           :math:`GDX_{i} = R \cdot \arccos[\sin\lambda_{i} \cdot \sin \lambda_{i-1} + \cos \varphi_{i}\cdot \cos \varphi_{i-1} \cdot \cos (\varphi_{i} -\varphi_{i-1})]`  

       Else if differenceType = BACKWARD then  

         :math:`GDX_{i} = R \cdot \arccos[\sin \lambda_{i} \cdot \sin \lambda_{i-1} + \cos \varphi_{i} \cdot \cos \varphi_{i-1} \cdot \cos (\varphi_{i} - \varphi_{i-1})]`  

           For the 1st level:  

           :math:`GDX_{i} = R \cdot \arccos[\sin \lambda_{i} \cdot \sin \lambda_{i+1} + \cos \varphi_{i} \cdot \cos \varphi_{i+1} \cdot \cos (\varphi_{i+1} - \varphi_{i})]`  

       End if  

   Else if axis = Y then  

       We proceed in the same way but with the points situated on the Y axis  
   
   End if

.. note::

   The latitudes and longitudes must be in radians in the trigonometric formula.

References:
~~~~~~~~~~~

-  `Great Circle <http://mathworld.wolfram.com/GreatCircle.html>`__

Keywords:
~~~~~~~~~

-  grille/grid, point, distance, centrée/centered, arrière/backward, avant/forward

Usage:
~~~~~~

.. code:: python

    import os
    import fstpy
    import spookipy

    spooki_dir  = os.environ['SPOOKI_DIR']
    tmpdir      = os.environ['BIG_TMPDIR']

    input_file  = (f'{spooki_dir}/pluginsRelatedStuff/GridPointDistance/testsFiles/inputFile.std')
    output_file = (f'{tmpdir}/outputFile.std')

    df = fstpy.StandardFileReader(input_file).to_pandas()

    res_df = spookipy.GridPointDistance(df, 
                                        axis=['x','y'], 
                                        difference_type='centered').compute()

    fstpy.StandardFileWriter(output_file, res_df).to_fst()
      

Contacts:
~~~~~~~~~

-  Author   : `Marc Klasa <https://wiki.cmc.ec.gc.ca/wiki/User:Klasam>`__
-  Coded by : `François Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support  : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginGridPointDistance.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginGridPointDistance.html>`_
