# `ansible-hosts`

## Purpose
Displays information on hosts from `ansible-inventory`.

## Syntax
```
Syntax: ansible-hosts [-h] [-c] [-n] [-v] [hosts [hosts ...]]
```

### Options and arguments
`hosts` is one or more regular expressions to select hosts.  By default, all hosts are turned.

| Option                         | Description                                             | Default                               |
|--------------------------------|---------------------------------------------------------|---------------------------------------|
| `-c`, `--commas`               | Join hosts with a comma.  `--name-only` is also implied | Print all information in tabular form |
| `-n`, `--names`, `-l`, `--list` | List names only, not even a heading                     | Print host names one line at a time   |
| `-v`                           | Enable verbose debugging                                | Debugging is not enabled              |

## Example

```
$ ansible-hosts
host           ip              user      key
bruno-amazon1  3.83.98.175     ec2-user  /home/mrbruno/.ssh/bruno.pem
bruno-amazon2  100.25.192.145  ec2-user  /home/mrbruno/.ssh/bruno.pem
bruno-rh8      100.26.227.68   ec2-user  /home/mrbruno/.ssh/bruno.pem
$ ansible-hosts ama
host           ip              user      key
bruno-amazon1  3.83.98.175     ec2-user  /home/mrbruno/.ssh/bruno.pem
bruno-amazon2  100.25.192.145  ec2-user  /home/mrbruno/.ssh/bruno.pem
$ ansible-hosts --names
bruno-amazon1
bruno-amazon2
bruno-rh8
$ echo $(ansible-hosts --names)
bruno-amazon1 bruno-amazon2 bruno-rh8
$ ansible-hosts --commas
bruno-amazon1,bruno-amazon2,bruno-rh8
$
```

### Making use of `--commas`
I often use `--names` or `--commas` when I'm using other tools.  Running an Ansible adhoc command is a good example:
```
$ echo ansible $(ansible-hosts -c) -m command -a hostname
ansible bruno-amazon1,bruno-amazon2,bruno-rh8 -m command -a hostname
$ ansible $(ansible-hosts -c) -m command -a hostname
bruno-amazon1 | SUCCESS | rc=0 >>
ip-172-31-86-19

bruno-amazon2 | SUCCESS | rc=0 >>
ip-172-31-49-27.ec2.internal

bruno-rh8 | SUCCESS | rc=0 >>
ip-172-31-58-255.ec2.internal

$
```

## Notes

- This assumes you have Ansible and an inventory file such as `/etc/ansible/hosts` that `ansible-inventory` can work with.
