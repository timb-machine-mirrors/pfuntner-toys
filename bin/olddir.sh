if [ "$BASH_SOURCE" != "$0" ]
then
  dir="$PWD"
  base=$(basename "$dir")
  if expr match "$base" '[0-9]\{23\}$' >/dev/null 2>&1
  then
    cd ..
    rm -rfv "$dir"
    echo "Back in $PWD"
  else
    echo "$PWD is not a 'new directory'" >&2
    false
  fi
else
  echo "not sourced" >&2
  false
fi
