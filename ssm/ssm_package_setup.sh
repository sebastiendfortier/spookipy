main(){
      load_runtime_dependencies
}

message(){
   echo $(tput -T xterm setaf 3)$@$(tput -T xterm sgr 0) >&2
   true
}

print_and_do(){
   message $@
   eval $@
}

load_runtime_dependencies(){
    message "Load ci_fstcomp for developpement"
    print_and_do . ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/fstpy/2.1.11/
    message '. ssmuse-sh -d /fs/ssm/eccc/cmd/cmds/apps/ci_fstcomp/(check directory for latest version)/'
}

main
