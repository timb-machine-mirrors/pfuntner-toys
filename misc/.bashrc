# This is a fragment of a bash script that I like to use in my $HOME/.bashrc

# Remove `ls` aliases
for cmd in $(alias | grep ls | awk -F'[ =]' '{ print $2 }')
do
  unalias $cmd
done

set -o vi
set -o ignoreeof

# alias br='vi -R'
alias r='fc -s'
alias more=less
alias width='tput cols'
alias copy=cp
alias newdir='dir=$(date +%Y%m%d%H%M%S%N) && mkdir -v $dir && cd $dir'
alias indent="$HOME/bin/indent"
alias pushsshkey=ssh-copy-id
alias time=ptime
alias table=table.py
alias gitbranch=currbranch
alias ansiblehost=ansiblehelper.py
alias color=color.py

# windoze aliases
if expr match "$(uname -s)" '.*[Ww][Ii][Nn]' >/dev/null 2>&1
then
  alias date=unixdate
fi

alias tools-setup="$HOME/repos/toys/misc/setup"

# alias for headingsort since i will try to call it various names
alias sortheadings=headingsort

function git_branch {
  git branch 2>/dev/null | awk '/^\*/ { print " " $2 }'
}
export CURRBRANCH=$(which currbranch 2>/dev/null)
if [ "X$CURRBRANCH" != X ]
then
  CURRBRANCH=$(truepath.py -u "$CURRBRANCH")
else
  CURRBRANCH=true
fi
# if [ "X$CURRBRANCH" = X ]
# then
#   CURRBRANCH=true
#   banner --color red 'Warning: Could not find the currbranch script' >&2
# fi
export PS1='[\u@\h \W`'$CURRBRANCH' --ps1`]\$ '

# My git frontend is not needed if you authenticate with an sshkey and use the ssh-style URL
# for the repo such as git@github.com:USER/REPO.git
#
# # Set up ~/bin/git as my `git` command rather than /usr/bin/git so it can auto-complete my user & token
# if test -f "$HOME/bruno/bin/git"
# then
#   alias git=$HOME/bruno/bin/git
# elif test -f "$HOME/bin/git"
# then
#   alias git=$HOME/bin/git
# fi

# Set alias for vi using my .exrc:
if test -f "$HOME/repos/toys/misc/.exrc"
then
  alias vi="vi -u $HOME/repos/toys/misc/.exrc"
fi
