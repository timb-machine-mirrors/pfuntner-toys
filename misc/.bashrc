
################################################################################
# This is a fragment of a bash script that I like to use in my $HOME/.bashrc   #
################################################################################

# Remove `ls` aliases
for cmd in $(alias | grep ls | awk -F'[ =]' '{ print $2 }')
do
  unalias $cmd
done

set -o vi
set -o ignoreeof # Don't logout if I hit CTRL-D accidentically at a prompt
set -o pipefail  # The exit status of a pipeline will be the rightmost command that failed

# Error if an undefined variable is used
#
# I tried setting this in my everyday user but had trouble doing a git rebase:
#
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool CCC-1923-3]$ git checkout master
#   Switched to branch 'master'
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool master]$ git pull
#   remote: Enumerating objects: 28, done.
#   remote: Counting objects: 100% (28/28), done.
#   remote: Compressing objects: 100% (17/17), done.
#   remote: Total 28 (delta 15), reused 20 (delta 11), pack-reused 0
#   Unpacking objects: 100% (28/28), done.
#   From wwwin-github.cisco.com:sto-ccc/cloud9-audit-tool
#      3110905..5622564  master     -> origin/master
#      74fc266..c8e0359  CCC-1926   -> origin/CCC-1926
#    * [new branch]      ccc1959    -> origin/ccc1959
#    * [new tag]         1.2.0      -> 1.2.0
#   Updating 3110905..5622564
#   Fast-forward
#    Release_Notes.md | 5 ++++-
#    1 file changed, 4 insertions(+), 1 deletion(-)
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool master]$ git checkout -
#   Switched to branch 'CCC-1923-3'
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool CCC-1923-3]$ git rebase master
#   First, rewinding head to replay your work on top of it...
#   Applying: CCC-1923-3: Correct test id's of EL7 prehardened skips
#   Using index info to reconstruct a base tree...
#   M   Release_Notes.md
#   Falling back to patching base and 3-way merge...
#   Auto-merging Release_Notes.md
#   CONFLICT (content): Merge conflict in Release_Notes.md
#   Failed to merge in the changes.
#   Patch failed at 0001 CCC-1923-3: Correct test id's of EL7 prehardened skips
#   The copy of the patch that failed is found in:
#      /home/centos/sto/repos/cloud9-audit-tool/.git/rebase-apply/patch
#
#   When you have resolved this problem, run "git rebase --continue".
#   If you prefer to skip this patch, run "git rebase --skip" instead.
#   To check out the original branch and stop rebasing, run "git rebase --abort".
#
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool (no branch, rebasing CCC-1923-3)]$ vi Relbash: !ref: unbound variable
#   bash: !ref: unbound variable
#   bash: words[i]: unbound variable
#   (venv) [centos@pfuntner-everyday cloud9-audit-tool (no branch, rebasing CCC-1923-3)]$
#
# It looks like it might be coming from /etc/bash_completion.d/git but I'm not sure how to fix it.
# I think it's best if this is not set.
#
# set -u

# alias br='vi -R'
alias r='fc -s'
alias more=less
alias width='tput cols'
alias copy=cp
alias indent="$HOME/bin/indent"
alias pushsshkey=ssh-copy-id
alias time=ptime
alias table=table.py
alias gitbranch=currbranch
alias instances=instances.py
alias docker-containers='docker ps --format "{{.Names}}"'
alias kill-docker-containers='docker ps -qa | xargs -r docker rm -f'

alias newdir='dir=$(date +%Y%m%d%H%M%S%N) && mkdir -v $dir && cd $dir'
alias olddir='. olddir.sh'
alias olddirs='find . -name "[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"'

alias ansiblehost=ansiblehelper.py
alias color=color.py
alias truepath=truepath.py

# alias zip=unzip

alias vact='. venv/bin/activate'

alias fixed2json='table.py -i fixed --headings -o json'
alias fixed2sep='table.py -i fixed --headings -o sep --sep \|'
alias fixed2markdown='table.py -i fixed --headings -o markdown'

unalias docker 2>/dev/null
# set up docker alias if docker is not available but podman is
if podman --version >/dev/null 2>&1 && ! docker --version >/dev/null 2>&1
then
  alias docker=podman
  export DOCKER=podman
elif docker --version >/dev/null 2>&1
then
  export DOCKER=docker
fi

# This is a nice command to ping all the machines in /etc/ansible/hosts.  I've since replaced it by bin/pingall but it's a good example of my tools
#
# Example output:
#   host    result  ansible_facts                                                       changed ping
#   centos8 SUCCESS {u'discovered_interpreter_python': u'/usr/libexec/platform-python'} False   pong
#   rhel8   SUCCESS {u'discovered_interpreter_python': u'/usr/libexec/platform-python'} False   pong
#
# alias pingall='ansible all -m ping | ansible2json | table --in json --out fixed --order host,result | headingsort'

# windoze aliases
if expr match "$(uname -s)" '.*[Ww][Ii][Nn]' >/dev/null 2>&1
then
  alias date=unixdate
  alias uptime=win-uptime
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
export PS1='[\u@\h `date +%H:%M:%S` \W`"'$CURRBRANCH'" --ps1`]\$ '

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
  alias vi="vi -u '$HOME/repos/toys/misc/.exrc'"
fi

alias supercd='. supercd.sh'
