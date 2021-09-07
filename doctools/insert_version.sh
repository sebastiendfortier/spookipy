#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
ROOT_DIR=${DIR:0:${#DIR}-3}
echo ${ROOT_DIR}
cd ${DIR}
cd ../doc
VERSION=$(head -n 1 ${ROOT_DIR}VERSION)
echo ${VERSION}
cp install.rst install.rst.bk
cp usage.rst usage.rst.bk
sed -i 's/_VERSION_/'"${VERSION}"'/g' install.rst
sed -i 's/_VERSION_/'"${VERSION}"'/g' usage.rst
