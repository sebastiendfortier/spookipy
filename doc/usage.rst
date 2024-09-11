Using spookipy in scripts or Jupyter Lab/Notebook
-------------------------------------------------

.. code:: bash

    # load surgepy
    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
    # get spookipy ssm package
    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/2024.08.00/

use spookipy
~~~~~~~~~~~~

.. code:: python

    # inside your script
    import spookipy
    uv_df = spookipy.windmodulus(df).compute()

Example
~~~~~~~

.. code:: python

    data_path = prefix + '/data/'
    import fstpy
    import spookipy
    # setup your file to read
    records=fstpy.StandardFileReader(data_path + 'ttuvre.std').to_pandas()
    # display selected records in a rpn voir format
    fstpy.voir(records)
    # compute uv on the selected records
    uv_df = spookipy.windmodulus(records).compute()
    dest_path = '/tmp/out.std'
    # write the selected records to the output file
    fstpy.StandardFileWriter(dest_path,uv_df).to_fst()

