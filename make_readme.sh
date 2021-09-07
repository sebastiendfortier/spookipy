#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}

pandoc doc/intro.rst doc/requirements.rst doc/install.rst doc/usage.rst doc/contributing.rst doc/ssm.rst -o README.md
