# `undupe`

## Purpose
Removes duplicate punctuation and whitespace from stdin.  It will not touch alphanumeric chracters but if anything else appears more than once in a succession, they will be reduced to a single occurrence.

## Syntax
```
Syntax: undupe
```

### Options and arguments
There are no options or arguments

## Example

A _before_ example: output from an OpenStack CLI that formats a table column but it can be rather difficult to read, especially on a screen without a wide width:
```
$ nova list
+--------------------------------------+---------------------------------------+--------+------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------+
| ID                                   | Name                                  | Status | Task State | Power State | Networks                                                                                                                               |
+--------------------------------------+---------------------------------------+--------+------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------+
| fd1afc31-104b-41d9-8978-30122c9ddb97 | autoit-f-autovnf-jpfuntne-avf-1       | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.7; autoit-jcp_mgmt=40.101.13.9                                                                               |
| 1dd45d82-c774-497f-8211-14c2301f161f | autoit-f-autovnf-jpfuntne-avf-2       | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.9; autoit-jcp_mgmt=40.101.13.5                                                                               |
| fcdd375f-37e1-4885-8c0f-d4aadad64e6e | jcp_autovnf-em-jpfuntne-em-1          | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.10; autoit-jcp_mgmt=40.101.13.8                                                                              |
| ea9571a5-0430-4ad7-a2b3-7e50deabe5ba | jcp_autovnf-em-jpfuntne-em-2          | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.14; autoit-jcp_mgmt=40.101.13.14                                                                             |
| 448ef86b-0bac-4de1-9fd2-a2afb5d6aaa4 | jcp_autovnf-esc-jpfuntne-esc-1        | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.11; autoit-jcp_mgmt=40.101.13.18                                                                             |
| da2f282d-5088-4ac1-858a-9c9148eb01bc | jcp_autovnf-esc-jpfuntne-esc-2        | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.17; autoit-jcp_mgmt=40.101.13.13                                                                             |
| 65bcf434-476c-4886-aa5d-37546aa4dda4 | jcp_autovnf-vPC-DI-PGW-jpfuntne-cf1-0 | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.5; autoit-jcp_mgmt=40.101.13.15; di-internal1=192.168.10.200; di-internal2=192.168.11.49                     |
| f112de69-86a4-4a80-be62-88fb0f010a82 | jcp_autovnf-vPC-DI-PGW-jpfuntne-cf1-1 | ACTIVE | -          | Running     | autoit-jcp_orch=40.101.14.6; autoit-jcp_mgmt=40.101.13.21; di-internal1=192.168.10.197; di-internal2=192.168.11.55                     |
| 76388909-7c46-4c01-b3bc-862a034f0278 | jcp_autovnf-vPC-DI-PGW-jpfuntne-sf1-0 | ACTIVE | -          | Running     | service2=192.168.13.32; service1=192.168.12.109; autoit-jcp_orch=40.101.14.20; di-internal2=192.168.11.53; di-internal1=192.168.10.235 |
| d308c878-2c51-47a5-9a6d-23185983c9b6 | jpfuntne-autodeploy-6-3-1             | ACTIVE | -          | Running     | management=192.168.100.42, 10.225.202.207                                                                                              |
| 36a7f0f4-55b3-4524-b060-5f86892a84d4 | jpfuntne-autoit-6-3-1                 | ACTIVE | -          | Running     | management=192.168.100.41, 10.225.202.240                                                                                              |
+--------------------------------------+---------------------------------------+--------+------------+-------------+----------------------------------------------------------------------------------------------------------------------------------------+
$
```

An _after_ example using the same command with this script used as a filter:
```
$ nova list | undupe
+-+-+-+-+-+-+
| ID | Name | Status | Task State | Power State | Networks |
+-+-+-+-+-+-+
| fd1afc31-104b-41d9-8978-30122c9ddb97 | autoit-f-autovnf-jpfuntne-avf-1 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.7; autoit-jcp_mgmt=40.101.13.9 |
| 1dd45d82-c774-497f-8211-14c2301f161f | autoit-f-autovnf-jpfuntne-avf-2 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.9; autoit-jcp_mgmt=40.101.13.5 |
| fcdd375f-37e1-4885-8c0f-d4aadad64e6e | jcp_autovnf-em-jpfuntne-em-1 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.10; autoit-jcp_mgmt=40.101.13.8 |
| ea9571a5-0430-4ad7-a2b3-7e50deabe5ba | jcp_autovnf-em-jpfuntne-em-2 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.14; autoit-jcp_mgmt=40.101.13.14 |
| 448ef86b-0bac-4de1-9fd2-a2afb5d6aaa4 | jcp_autovnf-esc-jpfuntne-esc-1 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.11; autoit-jcp_mgmt=40.101.13.18 |
| da2f282d-5088-4ac1-858a-9c9148eb01bc | jcp_autovnf-esc-jpfuntne-esc-2 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.17; autoit-jcp_mgmt=40.101.13.13 |
| 65bcf434-476c-4886-aa5d-37546aa4dda4 | jcp_autovnf-vPC-DI-PGW-jpfuntne-cf1-0 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.5; autoit-jcp_mgmt=40.101.13.15; di-internal1=192.168.10.200; di-internal2=192.168.11.49 |
| f112de69-86a4-4a80-be62-88fb0f010a82 | jcp_autovnf-vPC-DI-PGW-jpfuntne-cf1-1 | ACTIVE | - | Running | autoit-jcp_orch=40.101.14.6; autoit-jcp_mgmt=40.101.13.21; di-internal1=192.168.10.197; di-internal2=192.168.11.55 |
| 76388909-7c46-4c01-b3bc-862a034f0278 | jcp_autovnf-vPC-DI-PGW-jpfuntne-sf1-0 | ACTIVE | - | Running | service2=192.168.13.32; service1=192.168.12.109; autoit-jcp_orch=40.101.14.20; di-internal2=192.168.11.53; di-internal1=192.168.10.235 |
| d308c878-2c51-47a5-9a6d-23185983c9b6 | jpfuntne-autodeploy-6-3-1 | ACTIVE | - | Running | management=192.168.100.42, 10.225.202.207 |
| 36a7f0f4-55b3-4524-b060-5f86892a84d4 | jpfuntne-autoit-6-3-1 | ACTIVE | - | Running | management=192.168.100.41, 10.225.202.240 |
+-+-+-+-+-+-+
$
```

This is a little more managable and easier to read.  Sure, there are advantages to the table too but if you grep out the lines with very long data that's making the table so wide to begin with, the remaining rows in the original output still have a lot of useless and unnecessary padding.  This script addresses that.

## Notes

- The script only reads from stdin.
- White space (except for newlines) are treated the same.  So if you have `' \t '` (space, tab, space), that will be replaced with a single space.  This is the only exception - each punctuation character is treated sepearately.
