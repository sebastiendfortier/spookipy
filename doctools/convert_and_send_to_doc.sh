#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}
DOC_DIR=${DIR:0:${#DIR}-8}doc
echo ${DOCDIR}
# for f in `ls *.org`
# do
#    echo 'converting '$f&&pandoc -s $f -o ${DOC_DIR}/${f%.org}.rst
# done

cd ../spookipy

for f in `find . -name '*.rst'`
do
   name=${f/.*\/}
   name=${name%.rst}
   lower_name=`echo $name|tr [:upper:] [:lower:]`
   file_to_write=../doc/$lower_name.rst
   rm $file_to_write
   eval printf '=%.0s' {1..${#name}} >> $file_to_write
   printf "\n" >> $file_to_write
   echo $name >> $file_to_write
   eval printf '=%.0s' {1..${#name}} >> $file_to_write
   printf "\n" >> $file_to_write
   echo .. include:: $name.rst >> $file_to_write
   printf "\n" >> $file_to_write
   echo "Python Module"  >> $file_to_write
   echo "-------------"  >> $file_to_write
   printf "\n" >> $file_to_write
   echo ".. automodule:: spookipy."$lower_name"."$lower_name >> $file_to_write
   echo "   :members:" >> $file_to_write
   printf "\n" >> $file_to_write
   echo 'copying '$f&&cp $f ../doc/${name}.rst
done
# ==================
# AddElementsByPoint
# ==================

# .. include:: AddElementsByPoint.rst

# Python Module
# -------------

# .. automodule:: spookipy.addelementsbypoint.addelementsbypoint
#    :members:
