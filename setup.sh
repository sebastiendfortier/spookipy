
# Check that the shell script is being sourced by attempting
# to use return outside a function, which can only be done in
# if the script is being sourced and not if is being run.
#
# The true is important here to clear the previous exit
# code.  Without this, doing `false ; source setup.sh`
# would enter this if and call exit.
if ! (true && (return 2>/dev/null)) ; then
    echo "$0 ERROR : This script must be sourced"
    exit 1
fi

# Ensure that Ordenv is loaded
if [[ $ORDENV_SETUP != 1 ]] ; then
    echo "${BASH_SOURCE[0]} ERROR : Ordenv setup must be done to load rpnpy"
    return 1
fi

use_spookipy(){
    use_spookipy_deps
    add_spookipy_to_pythonpath
}

add_spookipy_to_pythonpath(){
    # Note the use of python for portability.
    # On darwin, readlink does not have the -f option
    bash_source=$(python3 -c "import os; print(os.path.realpath('${BASH_SOURCE[0]}'))")
    this_dir=$(cd -P $(dirname $bash_source) 2>/dev/null && pwd)
    spookipy_packages_dir=$this_dir
    export PYTHONPATH=$spookipy_packages_dir:$PYTHONPATH
}

print_and_do(){
   message $@
   eval $@
}

use_spookipy_deps(){
    # spookipy uses low-level python binding for
    # librmn functions provided by rpnpy
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1 eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
    print_and_do . ssmuse-sh -d /fs/ssm/eccc/cmd/cmde/surge/surgepy/1.0.8/
    print_and_do . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/apps/ci_fstcomp/1.0.3
}

use_spookipy
