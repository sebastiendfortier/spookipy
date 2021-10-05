Getting the source code
-----------------------

.. code:: bash

    git clone git@gitlab.science.gc.ca:cmdw-spooki/spookipy.git
    # create a new branch
    git checkout -b my_change
    # modify the code
    # commit your changes
    # fetch changes
    git fetch
    # merge recent master
    git merge origin master
    # push your changes
    git push origin my_change

Then create a merge request on science's gitlab
https://gitlab.science.gc.ca/cmdw-spooki/spookipy/merge_requests

Testing
-------

.. code:: bash

    # From the $project_root/test directory of the project
    . activate spookipy_dev
    # get rmn python library
    . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
    # get fstpy ssm package
    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.6/
    python -m pytest

Building documentation
----------------------

.. code:: bash

    # This will build documentation in docs/build and there you will find index.html
    # make sure fstpy is in the PYTHONPATH
    # From the $project_root/doc directory of the project
    make clean
    make doc
