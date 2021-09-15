main(){
      load_spooki_runtime_dependencies
}

message(){
   echo $(tput -T xterm setaf 3)$@$(tput -T xterm sgr 0) >&2
   true
}

print_and_do(){
   message $@
   eval $@
}

load_spooki_runtime_dependencies(){
    message "Loading spookipy runtime dependencies ..."
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/migdep/5.1.1
    print_and_do . r.load.dot eccc/mrd/rpn/MIG/ENV/rpnpy/2.1.2
    print_and_do . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/apps/ci_fstcomp/1.0.0
    message "if you dont have fstpy, use the following package"
    message ". ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.6/"
    message "if you dont have pandas >= 1.0.0, use the following package"
    message ". ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/python_packages/python3.6/all/2021.07"
    message "... done loading spookipy runtime dependencies."
}

main
