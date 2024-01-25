unset files

if [ "$BASH_SOURCE" == "$0" ]
then
  color.py red "Note: $0 is not sourced" >&2
  false
else
  eval files=$(supercd.py --bash "$@" 2>/dev/tty)

  if [ ${#files[@]} -eq 1 ]
  then
    echo "${files[0]}"
    cd "${files[0]}"
  elif [ ${#files[@]} -eq 0 ]
  then
    color.py red "No matches for $@" >&2
    false
  else
    color.py red "Too many matches for $@" >&2
    false
    for file in "${files[@]}"
    do
      echo "  $file"
    done
  fi
fi
