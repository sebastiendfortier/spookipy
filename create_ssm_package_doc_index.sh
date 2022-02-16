#!/bin/bash
echo ""
echo ".. # define a hard line break for HTML"
echo ".. |br| raw:: html"
echo "   <br />"
echo ""
echo "      Indices and tables"
echo "      =================="
echo ""
echo "      * :ref:\`genindex\`"
echo "      * :ref:\`modindex\`"
echo "      * :ref:\`search\`"
echo ""
echo "      .. #currentmodule:: spookipy"
echo "      .. #autofuntion:: __init__"
echo ""
echo ".. include:: intro.rst"
echo ""
echo ""
echo "Documentation"
echo "-------------"
echo ""
echo "**Start here**"
echo ""
echo "* :doc:\`requirements\`"
echo "* :doc:\`install\`"
echo "* :doc:\`usage\`"
echo "* :doc:\`contributing\`"
echo "* :doc:\`ssm\`"
echo "* :doc:\`plugin_anatomy\`"
echo ""
echo ".. toctree::"
echo "   :maxdepth: 1"
echo "   :hidden:"
echo "   :caption: Start here"
echo ""
echo "   requirements"
echo "   install"
echo "   usage"
echo "   contributing"
echo "   ssm"
echo "   plugin_anatomy"
echo ""
echo "**Modules**"
echo ""

while read p; do
    if ! [[ $p == '#'* ]]
    then 
        p=$(echo $p| cut -d ' ' -f1)
        echo "* :doc:\`${p}\`"
    fi
done < plugin_list.txt

echo ""
echo ""
echo ".. toctree::"
echo "   :maxdepth: 1"
echo "   :hidden:"
echo "   :caption: Modules"
echo ""

while read p; do
    if ! [[ $p == '#'* ]]
    then 
        p=$(echo $p| cut -d ' ' -f1)
        echo "   ${p}"
    fi
done < plugin_list.txt

echo ""
echo "**Tutorial**"
echo ""
echo "* :doc:\`tutorial\`"
echo ""
echo ".. toctree::"
echo "   :maxdepth: 1"
echo "   :hidden:"
echo "   :caption: Tutorial"
echo ""
echo "   tutorial"
echo ""
echo "**Misc**"
echo ""
echo "* :doc:\`LICENSE\`"
echo ""
echo ".. toctree::"
echo "   :maxdepth: 1"
echo "   :hidden:"
echo "   :caption: Misc"
echo ""
echo "   LICENSE"
echo ""