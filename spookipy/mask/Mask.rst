Description:
~~~~~~~~~~~~

-  This plug-in creates a mask according to the threshold value(s)
   given.

Iteration method:
~~~~~~~~~~~~~~~~~

-  Point-by-point

Dependencies:
~~~~~~~~~~~~~

-  A field

Result(s):
~~~~~~~~~~

-  MASK field

Algorithm:
~~~~~~~~~~

.. code-block:: text

         For F,             an input field
         For thresholds[j], jth value given in the list of --thresholds option
         For operator[j],   jth value given in the list of --operators option
         For value[j],      jth value given in the list of --values option
         For nbTrios,       the total number of threshold, operator and value trios

         For each point of the input field (i)

         Initialize MASK = 0.0

         For j = 0 to (nbTrios - 1)

            If F[i]  Operators[j]  Thresholds[j]
               MASK[i]=Value[j]
            Endif

         End for

         End for

Reference:
~~~~~~~~~~

-  Does not apply

Keywords:
~~~~~~~~~

-  UTILITAIRE/UTILITY, masque/mask


Usage:
~~~~~~



.. code:: python

   python3

   import os
   import fstpy.all as fstpy
   import spookipy.all as spooki

   spooki_dir = os.environ['SPOOKI_DIR']

   user = os.environ['USER']

   df = fstpy.StandardFileReader(f'{spooki_dir}/pluginsRelatedStuff/Mask/testsFiles/inputFile.std').to_pandas()

   res_df = spooki.Mask(
      df,
      thresholds=[0.0,10.0,15.0,20.0],
      values=[0.0,10.0,15.0,20.0],
      operators=['>=','>=','>=','>=']).compute()


   fstpy.StandardFileWriter(f'/tmp/{user}/outputFile.std', res_df).to_fst()

Contacts:
~~~~~~~~~

-  Auteur(e) : `Marc Verville <https://wiki.cmc.ec.gc.ca/wiki/Marc_Verville>`__, / `Daniel Figueras <https://wiki.cmc.ec.gc.ca/wiki/Daniel_Figueras>`__
-  Codé par : `Louise Faust <https://wiki.cmc.ec.gc.ca/wiki/User:Faustl>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ / `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__


Spooki original documentation:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Francais <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_french_doc/html/pluginMask.html>`_

`English <http://web.science.gc.ca/~spst900/spooki/doc/master/spooki_english_doc/html/pluginMask.html>`_
