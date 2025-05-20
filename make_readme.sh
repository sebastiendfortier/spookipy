#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}

pandoc --include-before-body=doc/readme_no_edit.rst doc/intro.rst doc/requirements.rst doc/install.rst doc/usage.rst doc/contributing.rst doc/livraison.rst -o README.md
