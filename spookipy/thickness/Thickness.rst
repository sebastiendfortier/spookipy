Description:
~~~~~~~~~~~~

-  Calculation of the thickness between two levels of a given geopotential height field.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Column-by-column

Dependencies:
~~~~~~~~~~~~~

-  A geopotential height field, GZ (at least 2 levels)

Result(s):
~~~~~~~~~~

-  Thickness field DZ, with the same units as the source

Algorithm:
~~~~~~~~~~

.. code-block:: text

         Verify that the type of vertical coordinate of the input field corresponds to the "coordinateType" key passed as parameter
         if true, get from the input field, with the help of the Select plug-in, the levels passed as parameters and do for each point:
            DZ = ABS ( GZ(top) - GZ(base) )
         else
            exit the plugin with an error message
         end if

Reference:
~~~~~~~~~~

-  None

Keywords:
~~~~~~~~~

-  MÉTÉO/WEATHER, épaisseur/thickness, hauteur/height, géopotentielle/geopotential, niveau/level, différence/difference


Usage:
~~~~~~

.. code:: python
   
   import os
   import fstpy
   import spookipy

   spooki_dir  = os.environ['SPOOKI_DIR']
   tmpdir      = os.environ['BIG_TMPDIR']

   input_file  = (f'{spooki_dir}/pluginsRelatedStuff/Thickness/testsFiles/inputFile.std')
   output_file = (f'{tmpdir}/outputFile.std')

   df = fstpy.StandardFileReader(input_file).to_pandas()

   res_df = spookipy.Thickness(df, 
                               base=1.0,
                               top=0.8346,
                               coordinate_type='UNKNOWN').compute()

   fstpy.StandardFileWriter(output_file, res_df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by :`Zakaria Haimeur <https://wiki.cmc.ec.gc.ca/wiki/User:Haimeurz>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Français <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginThickness.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginThickness.html>`_
