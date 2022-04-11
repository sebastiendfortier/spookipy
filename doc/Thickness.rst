  @page pluginThickness Thickness
 
     \htmlonly
     <span style='position: absolute; right: 20px;'><a href="../../spooki_french_doc/html/pluginThickness.html">Francais</a></span>
     \endhtmlonly
 
     \htmlonly
     <iframe src="forward2python.php/spooki_create_dynamic_doc_parts/formatHeader/Thickness" width="100%" height=60 frameborder=0 scrolling=no></iframe>
     \endhtmlonly
 
     \htmlonly
     <script type="text/javascript">function resizeFrame(f){ f.style.height = f.contentWindow.document.body.scrollHeight + "px"; }</script>
     \endhtmlonly
 
     <b> Description: </b>
         @ssmbrief Thickness between two levels @endssmbrief
         - Calculation of the thickness between two levels of a given geopotential height field.
 
     <b> Iteration method: </b>
         - Column-by-column
 
     <b> Dependencies: </b>
         - A geopotential height field, GZ (at least 2 levels)
 
     <b> Result(s): </b>
         - Thickness field DZ, with the same units as the source
 
     <b> Algorithm: </b>
     @verbatim
         Verify that the type of vertical coordinate of the input field corresponds to the "coordinateType" key passed as parameter
         if true, get from the input field, with the help of the Select plug-in, the levels passed as parameters and do for each point:
                 DZ = ABS ( GZ(top) - GZ(base) )
         else
             exit the plug-in with an error message
         end if
     @endverbatim
     <b> Reference: </b>
         - Does not apply
 
     <b> Customizable condition: </b>
         - ...
 
     <b> Keywords: </b>
         - MÉTÉO/WEATHER, épaisseur/thickness, hauteur/height, géopotentielle/geopotential, niveau/level, différence/difference
 
     <b> Usage: </b>
                 \htmlonly<iframe id='usage' src="forward2python.php/spooki_create_dynamic_doc_parts/usage/Thickness" width="100%" frameborder=0 scrolling=no onload="resizeFrame(document.getElementById('usage'))"></iframe>\endhtmlonly
 
     </code></pre>
 
     <b> Call example: </b>
     <code><pre><span class="call_example">
         ...
         spooki_run "[ReaderStd --input $SPOOKI_DIR/pluginsRelatedStuff/Thickness/testsFiles/inputFile.std] >>
                     [Thickness --base 1.0 --top 0.8346 --coordinateType SIGMA_COORDINATE] >>
                     [WriterStd --output /tmp/$USER/outputFile.std]"
         ...
     </span></pre></code>
 
     <b> Results validation: </b>
         \htmlonly<iframe src="forward2python.php/spooki_create_dynamic_doc_parts/formatValidation/Thickness" width="100%" height=60 frameborder=0></iframe>\endhtmlonly
 
     <b> Contacts: </b>
         - Coded by  : <a Zakaria Haimeur</a>
         - Support   : <a class="el" href="https://wiki.cmc.ec.gc.ca/wiki/CMDW"> CMDW</a> /
                       <a class="el" href="https://wiki.cmc.ec.gc.ca/wiki/CMDS"> CMDS</a>
 
     Reference to @ref Thickness "Thickness"
     <sup><a href="Thickness_8cpp_source.html">[code]</a></sup>
 
     @ref ThicknessTests "Tests unitaires"
 
     <a class="el" href="Thickness_graph.png" target="blank">Evaluation tree</a>
 
     <b> Uses: </b><br>
     \htmlonly<iframe src="forward2python.php/spooki_create_dynamic_doc_parts/uses/Thickness" width="100%" height=60 frameborder=0></iframe>\endhtmlonly
 
     <b> Used by: </b><br>
     \htmlonly<iframe src="forward2python.php/spooki_create_dynamic_doc_parts/isusedby/Thickness" width="100%" height=60 frameborder=0></iframe>\endhtmlonly

