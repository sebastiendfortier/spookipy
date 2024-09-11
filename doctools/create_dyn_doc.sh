#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo ${DIR}
cd ${DIR}
DOC_DIR=${DIR:0:${#DIR}-8}doc
echo ${DOCDIR}

cd ../
VERSION=$(grep __version__ spookipy/__init__.py | awk '{print $3}' | tr -d "'")
cd doc
OUTPUT=usage.rst
rm -f $OUTPUT
echo "Using spookipy in scripts or Jupyter Lab/Notebook" >> $OUTPUT
echo "-------------------------------------------------" >> $OUTPUT
echo "" >> $OUTPUT
echo ".. code:: bash" >> $OUTPUT
echo "" >> $OUTPUT
echo "    # load surgepy" >> $OUTPUT
echo "    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/" >> $OUTPUT
echo "    # get spookipy ssm package" >> $OUTPUT
echo "    . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python/spookipy/$VERSION/" >> $OUTPUT
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
echo "    .  r.load.dot /fs/ssm/eccc/cmd/cmdw/PRIVATE/spookipy/bundle/$VERSION" >> $OUTPUT
