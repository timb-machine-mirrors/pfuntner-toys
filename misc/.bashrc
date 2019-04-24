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
if test -f "$HOME/bruno/bin/misc/.exrc"
then
  alias vi="vi -u $HOME/bruno/bin/misc/.exrc"
elif test -f "$HOME/bin/misc/.exrc"
then
  alias vi="vi -u $HOME/bin/misc/.exrc"
fi
