========================
Spooki: MinMaxLevelIndex
========================

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

`MinMaxLevelIndex <classMinMaxLevelIndex.html>`__

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

`Français <../../spooki_french_doc/html/pluginMinMaxLevelIndex.html>`__

**Description:**

-  Finds the index of the maximum and/or minimum value in the column or
   part of it.

**Iteration method:**

-  Column by column

**Dependance:**

-  Meteorological field (3D)
   **If** the –bounded key is activated:
-  Field of indexes of the lower limit, KBAS
-  Field of indexes of the upper limit, KTOP

**Result(s):**

-  The meteorological field (3D) received as input
-  A field with the indices, KMIN (2D), for which the value of the
   meteorological field is minimum
   **and/or**
-  A field with the indices, KMAX (2D), for which the value of the
   meteorological field is maximum

**Algorithm:**

.. code:: fragment

    If the key --bounded is not activated :
        KBAS = lowest level in the column
        KTOP = highest level in the column

    For each column and for the levels between KBAS and KTOP:
    (this is done from bottom to top or from top to bottom depending on the "--direction" option)

        If (minMax = MIN or BOTH)
            Loop for k between KBAS and KTOP
                If min > VAR[k] then 
                   min = VAR[k]
                   KMIN = k
                End if
            End loop
        End if

        If (minMax = MAX or BOTH)
            Loop for k between KBAS and KTOP
                If max < VAR[k] then 
                   max = VAR[k] 
                   KMAX = k
                End if
            End loop
        End if

    | ***Notes:***

    -  If several identical values of the max or min are found in a
       column, the first occurrence will be considered the min or the
       max. Depending on the "--direction" option, it will be the
       highest or lowest occurrence in the sample.
    -  When the values of KBAS and KTOP are equal to -1 (fields needed
       when using the "--bounded" option), the column will be ignored
       and the returned value will be -1.

    **Reference:**

    -  Does not apply

    **Keywords:**

    -  UTILITAIRE/UTILITY, minimum, maximum, niveau/level, vertical,
       borné/bounded

    **Usage:**

    **Call example:** ````

    ::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std] >>
                        [MinMaxLevelIndex --minMax MIN --direction ASCENDING] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
            ...

    ````

    ::

            ...
            spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/MinMaxLevelIndex/testsFiles/inputFile.std] >>
                        ( [Copy] + ( ([SetConstantValue --value MININDEX --bidimensional] >> [Zap --fieldName KBAS]) + ([SetConstantValue --value MAXINDEX --bidimensional] >> [Zap --fieldName KTOP]) ) ) >>
                        [MinMaxLevelIndex --bounded --minMax MIN --direction DESCENDING] >>
                        [WriterStd --output /tmp/$USER/outputFile.std]"
            ...

    **Results validation:**

    **Responsables:**

    -  Author : `Daniel
       Figueras <https://wiki.cmc.ec.gc.ca/wiki/User:Figuerasd>`__
       `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__
    -  Coded by : `Sébastien
       Fortier <https://wiki.cmc.ec.gc.ca/wiki/User:Fortiers>`__,
       Jonathan Cameron, `Guylaine
       Hardy <https://wiki.cmc.ec.gc.ca/wiki/User:Hardyg>`__
    -  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
       `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

    Reference to `MinMaxLevelIndex <classMinMaxLevelIndex.html>`__
    :sup:``[code] <MinMaxLevelIndex_8cpp_source.html>`__`

    Tests unitaires

    `Evaluation tree <MinMaxLevelIndex_graph.png>`__

    | **Uses:**

    | **Used by:**

    --------------

    Generated by  |doxygen| 1.8.13

.. raw:: html

   </div>

.. raw:: html

   </div>

.. |doxygen| image:: doxygen.png
   :class: footer
   :target: http://www.doxygen.org/index.html
