# `table`

## Purpose
Format standard input in the form of a table.  Various styles of input and output are supported which can be mixed together.

## Syntax
```
usage: table [-h] [-c | -s SEPARATOR | -f] [-H | -m | -b | -r | -j]
             [--headings] [--simple-headings] [--file FILENAME] [-v]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
| `-c` or `--csv`  | Expect CSV as input | There is no default input style |
| `-s SEPARATOR` or `--separator SEPARATOR`  | Use a regular expression to separate input columns | There is no default input style |
| `-f` or `--fixed`  | Expect fixed columns as input | There is no default input style |
| `-h` or `--html`  | Print output as HTML | There is no default output style |
| `-m` or `--markdown`  | Print output as [markdown](https://www.wikiwand.com/en/Markdown).  Popular in [Git](https://www.wikiwand.com/en/Git), [Slack](https://www.wikiwand.com/en/Slack_%28software%29) | There is no default output style |
| `-b` or `--bbcode`  | Print output as [BBCode](https://www.wikiwand.com/en/BBCode).  Popular with message board systems  | There is no default output style |
| `-j` or `--json`  | Print output as JSON | There is no default output style |
| `-r` or `--rotate`  | Print output in a _rotated_ style | There is no default output style |
| `--headings` | Expect the first row of input to be headings | Headings are not expected |
| `--simple-headings` | Parse headings row very simply, not trying to retain blanks | Headings are parsed in a way to try to preserve blanks embedded inside a heading string |
| `--file FILENAME` | Specify a file from which to read | By default the script reads from stdin if `--file` is not specified |
| `-v` or `--verbose` | Enable debugging | Debugging is not enabled |

## Example

### Input: regular expression / Output: JSON
```
$ df | head -5 | table -s \\s+ -j 
[
  [
    "Filesystem", 
    "1K-blocks", 
    "Used", 
    "Available", 
    "Use%", 
    "Mounted_on"
  ], 
  [
    "udev", 
    "8133756", 
    "0", 
    "8133756", 
    "0%", 
    "/dev"
  ], 
  [
    "tmpfs", 
    "1631580", 
    "2132", 
    "1629448", 
    "1%", 
    "/run"
  ], 
  [
    "/dev/sdb2", 
    "236102400", 
    "31740828", 
    "192345140", 
    "15%", 
    "/"
  ], 
  [
    "tmpfs", 
    "8157880", 
    "34564", 
    "8123316", 
    "1%", 
    "/dev/shm"
  ]
]
```
Note that this is a list of lists because the headings row were treated as just another row of input.
### Input: regular expression with headings / Output: JSON
```
$ df | head -5 | table -s \\s+ -j  --headings
[
  {
    "1K-blocks": "8133756", 
    "Available": "8133756", 
    "Filesystem": "udev", 
    "Mounted_on": "/dev", 
    "Use%": "0%", 
    "Used": "0"
  }, 
  {
    "1K-blocks": "1631580", 
    "Available": "1629448", 
    "Filesystem": "tmpfs", 
    "Mounted_on": "/run", 
    "Use%": "1%", 
    "Used": "2132"
  }, 
  {
    "1K-blocks": "236102400", 
    "Available": "192345136", 
    "Filesystem": "/dev/sdb2", 
    "Mounted_on": "/", 
    "Use%": "15%", 
    "Used": "31740832"
  }, 
  {
    "1K-blocks": "8157880", 
    "Available": "8123452", 
    "Filesystem": "tmpfs", 
    "Mounted_on": "/dev/shm", 
    "Use%": "1%", 
    "Used": "34428"
  }
]
$ 
```
By using the `--headings` option, we now get a list of dictionaries and the heading for each column is used for the keys of the dictionaries.
### Input: regular expression with headings / Output: HTML
```
$ df | head -5 | table -s \\s+ --html  --headings
<table border='1'>
<tbody>
<tr>
<th>Filesystem</th>
<th>1K-blocks</th>
<th>Used</th>
<th>Available</th>
<th>Use%</th>
<th>Mounted_on</th>
</tr>
<tr>
<td>udev</td>
<td>8133756</td>
<td>0</td>
<td>8133756</td>
<td>0%</td>
<td>/dev</td>
</tr>
<tr>
<td>tmpfs</td>
<td>1631580</td>
<td>2132</td>
<td>1629448</td>
<td>1%</td>
<td>/run</td>
</tr>
<tr>
<td>/dev/sdb2</td>
<td>236102400</td>
<td>31740804</td>
<td>192345164</td>
<td>15%</td>
<td>/</td>
</tr>
<tr>
<td>tmpfs</td>
<td>8157880</td>
<td>34536</td>
<td>8123344</td>
<td>1%</td>
<td>/dev/shm</td>
</tr>
</tbody>
</table>
```
Note that the `<th>` tags are used for the headings.  The output isn't especially pretty because it's meant to be rendered in a browser window but it should look good.
### Input: regular expression with headings / Output: BBCode
```
$ df | head -5 | table -s \\s+ --b  --headings
[table]
[tbody]
[tr]
[th]Filesystem[/th]
[th]1K-blocks[/th]
[th]Used[/th]
[th]Available[/th]
[th]Use%[/th]
[th]Mounted_on[/th]
[/tr]
[tr]
[td]udev[/td]
[td]8133756[/td]
[td]0[/td]
[td]8133756[/td]
[td]0%[/td]
[td]/dev[/td]
[/tr]
[tr]
[td]tmpfs[/td]
[td]1631580[/td]
[td]2132[/td]
[td]1629448[/td]
[td]1%[/td]
[td]/run[/td]
[/tr]
[tr]
[td]/dev/sdb2[/td]
[td]236102400[/td]
[td]31738668[/td]
[td]192347300[/td]
[td]15%[/td]
[td]/[/td]
[/tr]
[tr]
[td]tmpfs[/td]
[td]8157880[/td]
[td]34432[/td]
[td]8123448[/td]
[td]1%[/td]
[td]/dev/shm[/td]
[/tr]
[/tbody]
[/table]
$
```
This output looks kind of like HTML but there are some differences in the tags.  Internally, a shared piece of code is used to generate both output styles.
### Input: regular expression with headings / Output: rotated
```
$ df | head -5 | table -s \\s+ -r  --headings
000000 00 Filesystem                       udev
000000 01 1K-blocks                        8133756
000000 02 Used                             0
000000 03 Available                        8133756
000000 04 Use%                             0%
000000 05 Mounted_on                       /dev
000001 00 Filesystem                       tmpfs
000001 01 1K-blocks                        1631580
000001 02 Used                             2132
000001 03 Available                        1629448
000001 04 Use%                             1%
000001 05 Mounted_on                       /run
000002 00 Filesystem                       /dev/sdb2
000002 01 1K-blocks                        236102400
000002 02 Used                             31746856
000002 03 Available                        192339112
000002 04 Use%                             15%
000002 05 Mounted_on                       /
000003 00 Filesystem                       tmpfs
000003 01 1K-blocks                        8157880
000003 02 Used                             35592
000003 03 Available                        8122288
000003 04 Use%                             1%
000003 05 Mounted_on                       /dev/shm
```
My _rotated_ style is a little hard to describe but it basically prints every column of every row on a separate line, indicating the row and column numbers.  Since headings were specified, the heading also appears along on every line.
### Input: regular expression without headings / Output: rotated
```
$ df | head -5 | table -s \\s+ -r  
000000 00 Filesystem
000000 01 1K-blocks
000000 02 Used
000000 03 Available
000000 04 Use%
000000 05 Mounted_on
000001 00 udev
000001 01 8133756
000001 02 0
000001 03 8133756
000001 04 0%
000001 05 /dev
000002 00 tmpfs
000002 01 1631580
000002 02 2132
000002 03 1629448
000002 04 1%
000002 05 /run
000003 00 /dev/sdb2
000003 01 236102400
000003 02 31746880
000003 03 192339088
000003 04 15%
000003 05 /
000004 00 tmpfs
000004 01 8157880
000004 02 34432
000004 03 8123448
000004 04 1%
000004 05 /dev/shm
$ 
```
Without the `--headings` option, the rotated output is a little different but not much.
### Input: fixed width / Output: JSON
```
$ ls -l | drop 1 | table --simple -f -j | head -40
[
  [
    "-rwxr-xr-x", 
    "1", 
    "mrbruno", 
    "mrbruno", 
    "1440", 
    "Jan", 
    "26", 
    "07:15", 
    "abspath"
  ], 
  [
    "-rwxr-xr-x", 
    "1", 
    "mrbruno", 
    "mrbruno", 
    "2771", 
    "Mar", 
    "29", 
    "18:04", 
    "acp"
  ], 
  [
    "-rwxr-xr-x", 
    "1", 
    "mrbruno", 
    "mrbruno", 
    "999", 
    "Aug", 
    "11", 
    "2018", 
    "addcrs"
  ], 
```
While coming up with this example, I actually had to add the `--simple-headings` option to treat the `ls` output a little differently because the headings were so close together.  I had code to try to retain embedded blanks in heading strings and the `--simple-headings` option disables that code.

Note this example makes use of my [`drop`](drop.md) tool.
### Input: CSV / Output: JSON
```
$ head -5 /home/mrbruno/repos/iyt/csv/20190407_102324_846368.csv 
Category,Game,GameID,User,UserID,WinLoss,Moves,Color,Date,Time
Regular,Anti-Backgammon,15300064812762,Donna D,15200000663034,Win,189,white,18/12/16,16:58:00
Regular,Anti-Backgammon,15300065319531,Danny Bad Boy,15200000782400,Win,31,black,18/08/28,08:53:00
Regular,Anti-Backgammon,15300064893256,supermanwuvsme,15200003044703,Win,290,black,18/07/05,22:28:00
Regular,Anti-Backgammon,15300064965692,pandagirl,15200003408150,Win,11,white,18/05/20,17:58:00
$ head -5 /home/mrbruno/repos/iyt/csv/20190407_102324_846368.csv | table --csv -j --headings 
[
  {
    "Category": "Regular", 
    "Color": "white", 
    "Date": "18/12/16", 
    "Game": "Anti-Backgammon", 
    "GameID": "15300064812762", 
    "Moves": "189", 
    "Time": "16:58:00", 
    "User": "Donna D", 
    "UserID": "15200000663034", 
    "WinLoss": "Win"
  }, 
  {
    "Category": "Regular", 
    "Color": "black", 
    "Date": "18/08/28", 
    "Game": "Anti-Backgammon", 
    "GameID": "15300065319531", 
    "Moves": "31", 
    "Time": "08:53:00", 
    "User": "Danny Bad Boy", 
    "UserID": "15200000782400", 
    "WinLoss": "Win"
  }, 
  {
    "Category": "Regular", 
    "Color": "black", 
    "Date": "18/07/05", 
    "Game": "Anti-Backgammon", 
    "GameID": "15300064893256", 
    "Moves": "290", 
    "Time": "22:28:00", 
    "User": "supermanwuvsme", 
    "UserID": "15200003044703", 
    "WinLoss": "Win"
  }, 
  {
    "Category": "Regular", 
    "Color": "white", 
    "Date": "18/05/20", 
    "Game": "Anti-Backgammon", 
    "GameID": "15300064965692", 
    "Moves": "11", 
    "Time": "17:58:00", 
    "User": "pandagirl", 
    "UserID": "15200003408150", 
    "WinLoss": "Win"
  }
]
$ 
```
This input file is a list of games I've played.
## Notes

- There was no `--file` option until I had to debug an issue with the PyCharm debugger and had no way to feed input through a pipeline.  Otherwise, there wouldn't be such an option!
