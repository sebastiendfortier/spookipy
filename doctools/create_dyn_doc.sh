#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}
DOC_DIR=${DIR:0:${#DIR}-8}doc
echo ${DOCDIR}

cd ../
VERSION_FILE="spookipy/__init__.py"
VERSION=$(grep __version__ $VERSION_FILE|cut -d"=" -f2)
year=$(echo $VERSION | cut -d '.' -f 1)
month=$(echo $VERSION | cut -d '.' -f 2)
version_part=$(echo $VERSION | cut -d '.' -f 3)
spooki_version_bundle=$year$month$version_part
spooki_version_ssm=$year$month'/'$version_part

echo "spooki_version_ssm = $spooki_version_ssm"
echo "spooki_version_bundle = $spooki_version_bundle"

fstpy_version_line=$(cat fstpy_env.txt)
# Extract year, month and version (result: YYYY.MM.VV)
yearmm=$(echo "$fstpy_version_line" | grep -oP '/fs/ssm/eccc/cmd/cmds/fstpy/bundle/\K\d{8}')
year="${yearmm:0:4}"
month="${yearmm:4:2}"
vv="${yearmm:6:2}"
fstpy_version="$year.$month.$vv"

# Extract year, month and version (result: YYYY.MM.VV)
ci_fstcomp_version=$(grep -E 'ci_fstcomp.*/[0-9]{6}/[0-9]{2}' ci_fstcomp.txt | sed -E 's|.*/ci_fstcomp/([0-9]{4})([0-9]{2})/([0-9]{2})|\1.\2.\3|')

OUTPUT=spookipy_env.txt
rm -f $OUTPUT
echo "    # SpookiPy and dependencies" >> $OUTPUT
echo "    .  r.load.dot /fs/ssm/eccc/cmd/cmdw/PRIVATE/spookipy/bundle/${spooki_version_bundle//\"/}" >> $OUTPUT

cd doc
OUTPUT=usage.rst
rm -f $OUTPUT
echo "Using spookipy in scripts or Jupyter Lab/Notebook" >> $OUTPUT
echo "-------------------------------------------------" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "$(cat ../cmds_python_env.txt)" >> $OUTPUT
echo "$(cat ../spookipy_env.txt)" >> $OUTPUT
echo "" >> $OUTPUT
echo "use spookipy" >> $OUTPUT
echo "~~~~~~~~~~~~" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: python" >> $OUTPUT
echo "" >> $OUTPUT
echo "    # inside your script" >> $OUTPUT
echo "    import spookipy" >> $OUTPUT
echo "    uv_df = spookipy.windmodulus(df).compute()" >> $OUTPUT
echo "" >> $OUTPUT
echo "Example" >> $OUTPUT
echo "~~~~~~~" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: python" >> $OUTPUT
echo "" >> $OUTPUT
echo "    data_path = prefix + '/data/'" >> $OUTPUT
echo "    import fstpy" >> $OUTPUT
echo "    import spookipy" >> $OUTPUT
echo "    # setup your file to read" >> $OUTPUT
echo "    records=fstpy.StandardFileReader(data_path + 'ttuvre.std').to_pandas()" >> $OUTPUT
echo "    # display selected records in a rpn voir format" >> $OUTPUT
echo "    fstpy.voir(records)" >> $OUTPUT
echo "    # compute uv on the selected records" >> $OUTPUT
echo "    uv_df = spookipy.windmodulus(records).compute()" >> $OUTPUT
echo "    dest_path = '/tmp/out.std'" >> $OUTPUT
echo "    # write the selected records to the output file" >> $OUTPUT
echo "    fstpy.StandardFileWriter(dest_path,uv_df).to_fst()" >> $OUTPUT
echo "" >> $OUTPUT

OUTPUT=install.rst
rm -f $OUTPUT
echo "Installation" >> $OUTPUT
echo "============" >> $OUTPUT
echo "" >> $OUTPUT
echo "Use the ssm package" >> $OUTPUT
echo "" >> $OUTPUT
echo "::" >> $OUTPUT
echo "" >> $OUTPUT
echo "$(cat ../spookipy_env.txt)" >> $OUTPUT


OUTPUT=contributing.rst
rm -f $OUTPUT
echo "Getting the source code" >> $OUTPUT
echo "-----------------------" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "    git clone git@gitlab.science.gc.ca:cmdw-spooki/spookipy.git  " >> $OUTPUT
echo "    # create a new branch  " >> $OUTPUT
echo "    git checkout -b my_change  " >> $OUTPUT
echo "    # modify the code  " >> $OUTPUT
echo "    # commit your changes  " >> $OUTPUT
echo "    # fetch changes  " >> $OUTPUT
echo "    git fetch  " >> $OUTPUT
echo "    # merge recent master  " >> $OUTPUT
echo "    git merge origin/master  " >> $OUTPUT
echo "    # push your change  " >> $OUTPUT
echo "    git push origin my_change  " >> $OUTPUT
echo "" >> $OUTPUT
echo "Then create a merge request on science's gitlab " >> $OUTPUT
echo "https://gitlab.science.gc.ca/cmdw-spooki/spookipy/merge_requests" >> $OUTPUT
echo "" >> $OUTPUT
echo "Testing" >> $OUTPUT
echo "-------" >> $OUTPUT
echo "" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "$(cat ../cmds_python_env.txt)" >> $OUTPUT
echo "$(cat ../fstpy_env.txt)" >> $OUTPUT
echo "$(cat ../ci_fstcomp.txt)" >> $OUTPUT
echo "    # From the \$project_root/test directory of the project" >> $OUTPUT
echo "    python -m pytest  " >> $OUTPUT
echo "" >> $OUTPUT
echo "Building documentation" >> $OUTPUT
echo "----------------------" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "    # This will build documentation in docs/build and there you will find index.html  " >> $OUTPUT
echo "    # Make sure fstpy is in the PYTHONPATH " >> $OUTPUT
echo "    # From the \$project_root/doc directory of the project " >> $OUTPUT
echo "    cd doc  " >> $OUTPUT
echo "    make clean " >> $OUTPUT
echo "    make doc  " >> $OUTPUT


OUTPUT=requirements.rst
rm -f $OUTPUT
echo "Requirements" >> $OUTPUT
echo "============" >> $OUTPUT
echo "" >> $OUTPUT
echo "run time packages" >> $OUTPUT
echo "-----------------" >> $OUTPUT
echo "- fstpy>=$fstpy_version" >> $OUTPUT
echo "- pandas>=1.5.1" >> $OUTPUT
echo "- numpy>=1.24.4" >> $OUTPUT
echo "- xarray>=2023.7.0" >> $OUTPUT
echo "- dask>=2023.7.1" >> $OUTPUT
echo "" >> $OUTPUT
echo "developpement packages" >> $OUTPUT
echo "----------------------" >> $OUTPUT
echo "- fstpy>=$fstpy_version" >> $OUTPUT
echo "- ci_fstcomp>=$ci_fstcomp_version" >> $OUTPUT
echo "- pandas>=1.5.1" >> $OUTPUT
echo "- numpy>=1.24.4" >> $OUTPUT
echo "- xarray>=2023.7.0" >> $OUTPUT
echo "- dask>=2023.7.1" >> $OUTPUT

echo "- pytest>=7.4.0" >> $OUTPUT
echo "- sphinx>=5.3.0" >> $OUTPUT
echo "- sphinx_autodoc_typehints>=1.21.8" >> $OUTPUT
echo "- sphinx_gallery>=0.13.0" >> $OUTPUT
echo "- sphinx_rtd_theme>=0.5.1" >> $OUTPUT
echo "- nbsphinx>=0.9.2" >> $OUTPUT
echo "" >> $OUTPUT

echo "CMDS Python environment" >> $OUTPUT
echo "-----------------------" >> $OUTPUT
echo "" >> $OUTPUT
echo "This is an ssm package that we use at CMC on the science network and
that contains a wide variety of packages" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "$(cat ../cmds_python_env.txt)" >> $OUTPUT
