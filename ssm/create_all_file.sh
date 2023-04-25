#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ROOT_DIR=${DIR:0:${#DIR}-3}
# echo $ROOT_DIR
cd ${DIR}


all_file=${ROOT_DIR}/spookipy/'all.py'
echo '# -*- coding: utf-8 -*-' >> ${all_file}
while read p; do
    if ! [[ $p == '#'* ]]
    then 
        p=$(echo $p| cut -d ' ' -f1)
        echo 'from .'$p' import *'  >> ${all_file}
    fi
done < ${ROOT_DIR}/plugin_list.txt

echo ''  >> ${all_file}
echo 'from .utils import *'  >> ${all_file}


