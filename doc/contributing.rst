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
    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
    # get fstpy ssm package
    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.10/
    python -m pytest

Building documentation
----------------------

.. code:: bash

    # This will build documentation in docs/build and there you will find index.html
    # make sure fstpy is in the PYTHONPATH
    # From the $project_root/doc directory of the project
    make clean
    make doc
