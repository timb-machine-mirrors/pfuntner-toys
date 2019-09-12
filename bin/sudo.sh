# This script will be used from aliases to get to run commands like minikube and kubectl from root.  I want an informational message reminding me this is happening.
echo \> sudo "$@" \< >&2
sudo "$@"
