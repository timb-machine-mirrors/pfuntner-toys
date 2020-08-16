# `ansible-role`

## Purpose
Execute an Ansible role without having to create the playbook

## Syntax
```
Syntax: ansible-role [-h] [-V] [-b] [-e EXTRA_VARS] [-d] [-v] role host [host ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-V`, `--ansible-verbose` | Use Ansible `-v` option - zero or more occurrences |
| `-b`, `--become` | Become root on hosts via `sudo` |
| `-e EXTRA_VARS`, `--extra-vars EXTRA_VARS` | One or more sets of extra variables to `ansible-playbook` |
| `-d`, `--dry-run` | Do not invoke `ansible-playbook` |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example

### Simple example
```
$ find . -type f | xargs grep '' -H
./myrole/tasks/main.yml:- name: Task 1
./myrole/tasks/main.yml:  debug:
./myrole/tasks/main.yml:    msg: "This is from Task 1: myvar={{ myvar | default('n/a') }}"
$ ansible-role myrole localhost

PLAY [Run myrole] ********************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************
ok: [localhost]

TASK [myrole : Task 1] ***************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "This is from Task 1: myvar=n/a"
}

PLAY RECAP ***************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   

$
```

### Debugging with an extra variable
```
$ ansible-role -vv -e myvar=foo myrole localhost
2020-08-16 10:39:41,417 INFO /home/mrbruno/bin/ansible-role:26 host: 'localhost'
2020-08-16 10:39:41,418 INFO /home/mrbruno/bin/ansible-role:28 Temporary playbook: '/tmp/tmp0fs5y8ua'
- name: Run myrole
  hosts: localhost
  roles:
  - role: myrole
2020-08-16 10:39:41,419 DEBUG /home/mrbruno/bin/ansible-role:47 ['ansible-playbook', '-e', 'myvar=foo', '/tmp/tmp0fs5y8ua']

PLAY [Run myrole] ********************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************
ok: [localhost]

TASK [myrole : Task 1] ***************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "This is from Task 1: myvar=foo"
}

PLAY RECAP ***************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   

$
```

### `ansible-playbook` debugging
```
$ ansible-role -VV -vv ~-/myrole localhost
2020-08-16 10:51:18,952 INFO /home/mrbruno/bin/ansible-role:26 host: 'localhost'
2020-08-16 10:51:18,953 INFO /home/mrbruno/bin/ansible-role:28 Temporary playbook: '/tmp/tmpj2jc9mij'
- name: Run /home/mrbruno/tmp/20200816102653672382905/myrole
  hosts: localhost
  roles:
  - role: /home/mrbruno/tmp/20200816102653672382905/myrole
2020-08-16 10:51:18,954 DEBUG /home/mrbruno/bin/ansible-role:47 ['ansible-playbook', '-v', '-v', '/tmp/tmpj2jc9mij']
ansible-playbook 2.5.1
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/mrbruno/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python2.7/dist-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 2.7.17 (default, Jul 20 2020, 15:37:01) [GCC 7.5.0]
Using /etc/ansible/ansible.cfg as config file

PLAYBOOK: tmpj2jc9mij ****************************************************************************************************************************************************
1 plays in /tmp/tmpj2jc9mij

PLAY [Run /home/mrbruno/tmp/20200816102653672382905/myrole] **************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************
task path: /tmp/tmpj2jc9mij:1
ok: [localhost]
META: ran handlers

TASK [/home/mrbruno/tmp/20200816102653672382905/myrole : Task 1] *********************************************************************************************************
task path: /media/mrbruno/ExtraDrive1/tmp/20200816102653672382905/myrole/tasks/main.yml:1
ok: [localhost] => {
    "msg": "This is from Task 1: myvar=n/a"
}
META: ran handlers
META: ran handlers

PLAY RECAP ***************************************************************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0   

$ 
```

## Notes

- A temporary playbook is created and removed after running `ansible-playbook`.
- You can use a relative or full path to the role directory which just gets specified in the playbook. 