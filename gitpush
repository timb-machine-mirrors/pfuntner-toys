if [ $# -ne 1 ]
then
  echo "Syntax: $0 file" >&2
  exit 1
fi

if ! test -f "$1"
then
  echo "Cannot find '$1'" >&2
  exit 1
fi

if cd $(dirname "$1")
then
  banner "git add $1"
  if git add $(basename "$1")
  then
    banner "git commit"
    if git commit
    then
      banner "git push"
      git push
    fi
  fi
fi
