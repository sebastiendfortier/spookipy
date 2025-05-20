Creating the ssm package
========================

The "--yaml" option can be used to determine which plugins will be included in the ssm package.  

.. code:: bash

    # This will build the ssm package. 
    cd livraison  
    ./make_ssm_package.py  
    or 
    ./make_ssm_package.py --yaml <plugin_list.yaml>
