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

   python3
   from spookipy.thickness.thickness import Thickness,ParametersValuesError
   from test import TEST_PATH, TMP_PATH
   import fstpy.all as fstpy
   import spookipy.all as spooki
   import rpnpy.librmn.all as rmn

   plugin_test_dir = "/fs/site3/eccc/cmd/w/spst900/spooki/spooki_dir/pluginsRelatedStuff/"
   source0 = plugin_test_dir + "GZ_12000_10346_fileSrc.std"
   src_df0 = fstpy.StandardFileReader(source0,decode_metadata=True).to_pandas()
   df = Thickness(src_df0,base=1.0,top=0.8346,coordinate_type='UNKNOWN').compute()

   results_file = ''.join([TMP_PATH, secrets.token_hex(16), "test_1.std"])
   fstpy.delete_file(results_file)
   fstpy.StandardFileWriter(results_file, df).to_fst()

Contacts:
~~~~~~~~~

-  Author : `Hatem Yazidi <https://wiki.cmc.ec.gc.ca/wiki/User:Yazidih>`__
-  Coded by :`Zakaria Haimeur <https://wiki.cmc.ec.gc.ca/wiki/User:Haimeurz>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginThickness.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginThickness.html>`_
