#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}
DOC_DIR=${DIR:0:${#DIR}-3}doc
echo ${DOCDIR}
for f in `ls *.org`
do
   echo 'converting '$f&&pandoc -s $f -o ${DOC_DIR}/${f%.org}.rst
done

cd ../spookipy

for f in `find . -name '*.org'`
do 
   name=${f/.*\/}
    echo 'converting '$f&&pandoc -s $f -o ../doc/${name%.org}.rst
done
