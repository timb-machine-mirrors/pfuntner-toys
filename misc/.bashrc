# This is a fragment of a bash script that I like to use in my $HOME/.bashrc

# Remove `ls` aliases
for cmd in $(alias | grep ls | awk -F'[ =]' '{ print $2 }')
do
  unalias $cmd
done

set -o vi
alias br='vi -R'
alias r='fc -s'
alias more=less

# Set up ~/bin/git as my `git` command rather than /usr/bin/git so it can auto-complete my user & token
alias git=$HOME/bin/git
