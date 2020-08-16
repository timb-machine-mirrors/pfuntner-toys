# `ansible-host-data`

## Purpose
Displays a specific piece of information about a host in `ansible-inventory`

## Syntax
```
Syntax: ansible-host-data [-h] (-u | -i | -k) [-v] host
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-u`, `--user` | Extract user - the `ansible_user` attribute from the inventory file | You must select one extraction option |
| `-i`, `--ip` | Extract IP - the `ansible_host` attribute from the inventory file.<br/><br/>The attribute may not even be an _IP_ address but I thought that would be more clear than the friendly hostname given as a key in the inventory. | You must select one extraction option |
| `-k`, `--key` | Extract key - the `ansible_ssh_private_key_file` attribute from the inventory file | You must select one extraction option |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

```
$ cat /etc/ansible/hosts
[targets]
bruno-amazon1 ansible_host=3.84.84.102 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
bruno-amazon2 ansible_host=18.234.193.98 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
bruno-rh8 ansible_host=34.207.227.119 ansible_user=ec2-user ansible_ssh_private_key_file=/home/mrbruno/.ssh/bruno.pem
$ ansible-inventory --list -y
all:
  children:
    targets:
      hosts:
        bruno-amazon1:
          ansible_host: 3.84.84.102
          ansible_ssh_private_key_file: /home/mrbruno/.ssh/bruno.pem
          ansible_user: ec2-user
        bruno-amazon2:
          ansible_host: 18.234.193.98
          ansible_ssh_private_key_file: /home/mrbruno/.ssh/bruno.pem
          ansible_user: ec2-user
        bruno-rh8:
          ansible_host: 34.207.227.119
          ansible_ssh_private_key_file: /home/mrbruno/.ssh/bruno.pem
          ansible_user: ec2-user
    ungrouped: {}
$ ansible-hosts
host           ip              user      key
bruno-amazon1  3.84.84.102     ec2-user  /home/mrbruno/.ssh/bruno.pem
bruno-amazon2  18.234.193.98   ec2-user  /home/mrbruno/.ssh/bruno.pem
bruno-rh8      34.207.227.119  ec2-user  /home/mrbruno/.ssh/bruno.pem
$ ansible-host-data -i bruno-rh8
34.207.227.119
$ ansible-host-data -k bruno-rh8
/home/mrbruno/.ssh/bruno.pem
$ ansible-host-data -u bruno-rh8
ec2-user
$ 
```

## Notes

- This assumes you have Ansible and an inventory file such as `/etc/ansible/hosts` that `ansible-inventory` can work with.
