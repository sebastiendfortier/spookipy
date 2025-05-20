Release
========

Update release version number
-----------------------------

.. code:: bash

   Update the version number in spookipy/__init__.py 

Update configuration files
--------------------------
.. code:: bash

   Update the following configuration files:

      * cmds_python_env.txt:  CMDS python environment
      * fstpy_env.txt:  FSTPY and dependencies
      * ci_fstcomp.txt: ci_fstcomp version

Build documentation
-------------------
.. code:: bash

   cd doc  
   make clean 
   make doc  

Commit changes
--------------
.. code:: bash

   Commit the following files:

   * README.md
   * fstpy_env.txt
   * cmds_python_env.txt
   * ci_fstcomp.txt

.. include:: ssm.rst
