# `undent`

## Purpose
This tool removes indentation from stdin.  It scans all the lines and calculates the maximum number of leading blanks that all the lines have in common.  It then prints out the lines with those leading blanks removed.

## Syntax
```
Syntax: undent
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Example
I'll describe a _use case_ that drove me to create this tool.  I had a block of code with indentation.  I think it was Jenkins Groovy code but it could have been anything.  It was indented pretty significantly and I wanted to include it in a Slack message (well, probably not _Slack_ but something analogous) but didn't want to have to deal with removing all the indentation by hand.

Once I had such a tool, I pasted the source lines into a file and had the tool process the file
```
$ cat tmp.txt
            else:
              match = operation_regexp.search(line)
              if match:
                tokens = match.groups()
                self.log.debug(f'Checking for file status in {tokens}')
                if tokens[0] == 'A':
                  commits[-1]['files'].append({'operation': 'add', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'M':
                  commits[-1]['files'].append({'operation': 'modify', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'D':
                  commits[-1]['files'].append({'operation': 'delete', 'name': self.repair_filename(tokens[1])})
                elif tokens[0] == 'Merge:':
                  commits[-1]['merge'].append(tokens[1:] if tokens[2] else tokens[1].split())
                elif tokens[0].startswith('R'):
                  commits[-1]['files'].append({
                    'operation': 'rename',
                    'old_name': self.repair_filename(tokens[1]),
                    'name': self.repair_filename(tokens[2])
                  })

$ undent < tmp.txt
else:
  match = operation_regexp.search(line)
  if match:
    tokens = match.groups()
    self.log.debug(f'Checking for file status in {tokens}')
    if tokens[0] == 'A':
      commits[-1]['files'].append({'operation': 'add', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'M':
      commits[-1]['files'].append({'operation': 'modify', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'D':
      commits[-1]['files'].append({'operation': 'delete', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'Merge:':
      commits[-1]['merge'].append(tokens[1:] if tokens[2] else tokens[1].split())
    elif tokens[0].startswith('R'):
      commits[-1]['files'].append({
        'operation': 'rename',
        'old_name': self.repair_filename(tokens[1]),
        'name': self.repair_filename(tokens[2])
      })

$ undent -v < tmp.txt
2022-03-12 09:20:52,422 INFO /home/mrbruno/bin/undent:34 num_blanks = 12
else:
  match = operation_regexp.search(line)
  if match:
    tokens = match.groups()
    self.log.debug(f'Checking for file status in {tokens}')
    if tokens[0] == 'A':
      commits[-1]['files'].append({'operation': 'add', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'M':
      commits[-1]['files'].append({'operation': 'modify', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'D':
      commits[-1]['files'].append({'operation': 'delete', 'name': self.repair_filename(tokens[1])})
    elif tokens[0] == 'Merge:':
      commits[-1]['merge'].append(tokens[1:] if tokens[2] else tokens[1].split())
    elif tokens[0].startswith('R'):
      commits[-1]['files'].append({
        'operation': 'rename',
        'old_name': self.repair_filename(tokens[1]),
        'name': self.repair_filename(tokens[2])
      })

$
```

## Notes

- The tool only reads from stdin so you must redirect from a pipe or in a pipeline.
