source ~spst900/spooki/use_nb_master_python.dot

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

current_base_path="$(cd "$(dirname ${real_file})/"; pwd)"
echo $current_base_path

export PYTHONPATH=$current_base_path:$PYTHONPATH

