main(){
  if ! require_ordenv_loaded ; then return 1 ; fi


  if ((${#BASH_SOURCE[@]})); then
      #bash
      shell_source=${BASH_SOURCE[0]}
  elif ((${#KSH_VERSION[@]})); then
      #ksh
      shell_source=${.sh.file}
  fi

  sourced_file="$(cd "$(dirname "${shell_source}")"; pwd -P)/$(basename "${shell_source}")"

  in_ssm=false
  if [ -d "$(dirname ${sourced_file})/../../../etc/ssm.d" ] ; then
      in_ssm=true
  fi

  if $in_ssm ; then
      real_file=${sourced_file}
  else
      real_file=$(readlink -f ${sourced_file})
  fi

  base_path="$(cd "$(dirname ${real_file})/../.."; pwd)"

  if in_build_dir ; then
      message "ERROR: This script is only meant for the installed version of spookipy. "
      return 2
  fi

  warn_override_variables PYTHONPATH

    CDIR=`pwd`
    cd $TMPDIR
    if ! [ -d 'ssm_python' ]; then
        mkdir ssm_python
    fi
    cd ssm_python
    for f in ${base_path}/lib/packages/*;
    do
        ln -s $f
    done
    cd $CDIR
    warn_override_variables PYTHONPATH

    SSM_PATH_PRESENT=$(echo $PYTHONPATH|grep ssm_python || test $? = 1;)

    if [ -z $SSM_PATH_PRESENT ]; then
        [ -z "$PYTHONPATH" ] && export PYTHONPATH=${TMPDIR}/ssm_python || export PYTHONPATH=${TMPDIR}/ssm_python:$PYTHONPATH
    fi

  if $in_ssm ; then
      load_project_runtime_dependencies
      message "SUCCESS: Using spookipy from ${base_path}"
  fi
}

message(){
   echo $(tput -T xterm setaf 3)${sourced_file}: $@$(tput -T xterm sgr 0) >&2
   true
}

require_ordenv_loaded(){
    if ! [ -v ORDENV_SETUP ] ; then
        message "ERROR: ORDENV_SETUP is not set, ordenv must be loaded to use spookipy."
        return 1
    fi
}

warn_override_variables(){
    for v in $@ ; do
        if [ -v $v ] ; then
            eval message "WARNING: Overriding variable $v \(previous value: \$$v\)"
        fi
    done
}

# check_directory_variables(){
#     missing_dir=0
#     for dv in $@ ; do
#         if eval ! [ -d \$$dv ] ; then
#             eval message "ERROR: Directory referenced by $dv does not exist \(\$$dv\)"
#             missing_dir=1
#         fi
#     done
#     return $missing_dir
# }

in_build_dir(){
    [ -e ${base_path}/CMakeFiles ]
}

print_and_do(){
   message $@
   eval $@
}

load_project_runtime_dependencies(){
    message "Loading spookipy runtime dependencies ..."
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
    #print_and_do python3 -m pip install -r ${base_path}/etc/profile.d/requirements.txt
    message "... done loading spookipy runtime dependencies."
}

main
