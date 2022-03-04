unset files

if [ "$BASH_SOURCE" == "$0" ]
then
  echo "Note: $0 is not sourced" >&2
fi

eval files=$(supercd.py --bash "$@")

if [ ${#files[@]} -eq 1 ]
then
  echo "${files[0]}"
  cd "${files[0]}"
elif [ ${#files[@]} -eq 0 ]
then
  echo "No matches for $@" >&2
else
  echo "Too many matches for $@" >&2
  for file in "${files[@]}"
  do
    echo "  $file"
  done
fi
