
################################################################################
# This is a fragment of a bash profile that I liked to use                     #
################################################################################
# 
# Remember that bash looks for profile scripts in the following order:
#   $HOME/.bash_profile
#   $HOME/.bash_login
#   $HOME/.profile

export PATH="$PATH:$HOME/repos/toys/bin"

local="$HOME/local/bin"
if test -e "$local"
then
  export PATH="$PATH:$local"
fi

export PAGER=less
export EDITOR=vi
export PYTHONUNBUFFERED=true

$HOME/bin/set-title --self 

# Windoze setup
if expr match "$(uname -s)" '.*[Ww][Ii][Nn]' >/dev/null 2>&1
then
  export ROOT=/cygdrive/c
  export GVIM=$ROOT/utils/gVimPortable/gVimPortable.exe
  export VIM=$ROOT/utils/gVimPortable/gVimPortable.exe
  export HOSTS=$ROOT/Windows/System32/drivers/etc/hosts
  export DOWNLOADS="$USERPROFILE/Downloads"
fi

# For shared systems, this is useful for automatically sourcing my personal setup script
#
# if [ "$($HOME/bruno/bin/incomingHost)" == "ibm750-r9rw756.raleigh.ibm.com" ]
# then
#   echo "$(hostname) welcomes Bruno"
#   source $HOME/bruno/setup
# fi

export GITHUB_USER=pfuntner

################################################################################
# This `true` statement should be last and will make sure that the this script #
# returns with success regardless of what the previous command was.            #
################################################################################
true
