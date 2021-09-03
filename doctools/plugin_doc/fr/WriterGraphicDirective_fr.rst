Français
--------

**Description:**

-  Produit un champ de directive WGD qui sera utilisé par le pour
   remplir le template associé à un produit. Le produit est identifier
   par l'argument --productName. Les templates se trouve dans le
   répertoire: $SPOOKI\ :sub:`RESSOURCESDIR`/WriterGraphic/productName/
   productName: argument du paramètre --productName Voir le plugin
   `WriterGraphic <../../spooki_french_doc/html/pluginWriterGraphic.html>`__
   pour plus d'information

\*Méthode d'itération:\*

-  N/D

\*Dépendances:\*

-  N/D

\*Résultat(s):\*

-  Un champ de directive WGD est produit

\*Algorithme:\*

-  N/D

\*Références:\*

-  N/D

\*Mots clés:\*

-  IO, directive, graphique/graphic, carte/map, writer

\*Usage:\*

**Exemple d'appel:**

.. code:: example

    ...
    spooki_run "[TrueOperation] || ([WriterGraphicDirective --productName 4pClassic --directive forecastHour:12,hourDelta:6,jobName:R1DFX03,runId:R1,runHour:00] >>
                [WriterStd --output /tmp/$USER/outputFile.std])"
    ...

**Validation des résultats:**

**Contacts:**

-  Auteur(e) : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Codé par : `François
   Fortin <https://wiki.cmc.ec.gc.ca/wiki/User:Fortinf>`__
-  Support : `CMDW <https://wiki.cmc.ec.gc.ca/wiki/CMDW>`__ /
   `CMDS <https://wiki.cmc.ec.gc.ca/wiki/CMDS>`__

Voir la référence à

Tests unitaires

| **Ce plugin utilise:**
| **Ce plugin est utilisé par:**

 
