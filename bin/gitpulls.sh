# Refresh my repositories
cd
for dir in repos/*
do
  if test -d "$dir"
  then
    banner $dir
    if cd "$HOME/$dir"
    then
      branch=$(git branch | awk '{ if ($1 == "*") print $2 }')
      if [ "X$branch" = Xmaster ]
      then
        git pull
        echo
      else
        cat <<EOF | banner --color lightred --center >&2
ATTENTION!
The branch of $dir is $branch, not master!
EOF
      fi
      cd - >/dev/null
    fi
  fi
done
