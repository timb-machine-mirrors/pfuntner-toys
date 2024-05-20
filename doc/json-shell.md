# `json-shell`

## Purpose
An interactive _shell-like_ tool to explore a JSON file.

I am often frustrated by large complicated JSON objects and had this wild idea of treating an object like a Unix filesystem: there is a root, child nodes, and grandchildren, you can navigate with `cd` along with other familiar Unix commands. 

## Syntax
```
Syntax: json-shell [-v] json-filename
```

### Options
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-v`  | Enable verbose debugging | Debugging is not enabled |

## Examples

Unlike a lot of my other tools, the examples are in the forms of interactive subcommands in the tool so I'll give examples of those.

Since there are so many subcommands and some of the help information is a little long, I'll provide a table of contents:

- [cat](#cat)
- [cd](#cd)
- [describe](#describe)
- [exit](#exit)
- [help](#help)
- [ls](#ls)
- [pwd](#pwd)

I'll also use the following JSON file in examples:
```json
{
  "bools": [true, false],
  "ints": [42, 32768, -1],
  "floats": [3.141592654, 2.7182818285, -0.000001],
  "strs": ["a", "b", "foo", "bar"],
  "none": null,
  "dict": {
    "1": [".", "one", "One", "ONE"],
    "2": ["..", "two", "Two", "TWO"]
  }
}
```

### The prompt
The tool prompts for subcommands includes the _current location_ much like the current working directory as in a filesystem.
```commandline
$ json-shell sample.json
Confoozed?  Try `help`
/> 
```
The location is `/` since you always begin in the root node.  The `> ` is asking for a subcommand to be entered.

### `help`
You can get general help of all subcommands:

```commandline
/> help
Navigate around a JSON document, just like a shell, only different!

Commands:

  cat       Display the current node or a child
              `cat` by itself displays the current node
              `cat key` display child element `key` of the current node

  cd        Change the current node
              `cd` by itself goes to root node
              `cd ..` go to parent node as long as you're not already at the root
              `cd key` goes to a child node if the key exists and its node is a dictionary or list

  describe  Describe a node
              `describe` describes the current node
              `describe key` describes the child element `key` of the current node

  exit      Exit from json-shell

  help      Display help

  ls        List keys in the current node

  pwd       Print the current node - note that this is included in each prompt

  quit      Exit from json-shell
/>
```

or you can get help on a specific subcommand:
```commandline
/> help cd
Change the current node
  `cd` by itself goes to root node
  `cd ..` go to parent node as long as you're not already at the root
  `cd key` goes to a child node if the key exists and its node is a dictionary or list
/> 
```

### `exit`
The `exit` and `quit` subcommands terminate the tool and return you to the Unix shell.  The subcommands are synonymous.

### `cd`
I'm taking great liberties with the name because we're not talking about a _current working directory_ but it's a similar concept.  You can `cd` into any child that's a list of dictionary itself:
```commandline
/> cd bools
/bools> cd ..
/> cd dict
/dict> cd 1
/dict/1> cd
/> 
```
The _keys_ you can `cd` into are based on the type of node you're currently in:
- If the current node is a dictionary, the keys of the dictionary are the keys you can cd into.
- If the current node is a list, the keys are integers from 0 to the length of the list minus one.  You don't have to treat the key differently just because it's an integer.

There are invalid `cd`s based on the current node:
```commandline
/> cd foo
'foo' is not a key
/> cd floats
/floats> cd 3
3 is out of range
/floats> cd -1
-1 is out of range
/floats> cd 0
0 is not a list or dictionary
/floats> 
```

### `ls`
The `ls` subcommand displays the keys of the current node:
```commandline
/> ls
bools  ints  floats  strs  none  dict
/> cd dict
/dict> ls
1  2
/dict> cd 1
/dict/1> ls
0  1  2  3
/dict/1> 
```

### `cat`
`cat` will display the current or target node and all of its children.

```commandline
/> cat
{
  "bools": [
    true,
    false
  ],
  "ints": [
    42,
    32768,
    -1
  ],
  "floats": [
    3.141592654,
    2.7182818285,
    -1e-06
  ],
  "strs": [
    "a",
    "b",
    "foo",
    "bar"
  ],
  "none": null,
  "dict": {
    "1": [
      ".",
      "one",
      "One",
      "ONE"
    ],
    "2": [
      "..",
      "two",
      "Two",
      "TWO"
    ]
  }
}
/> cd dict
/dict> cat
{
  "1": [
    ".",
    "one",
    "One",
    "ONE"
  ],
  "2": [
    "..",
    "two",
    "Two",
    "TWO"
  ]
}
/dict> cd 1
/dict/1> cat
[
  ".",
  "one",
  "One",
  "ONE"
]
/dict/1> 
```

### `describe`
The `describe` subcommand _describes_ the current or target node:
```commandline
/> describe
/ is a dict with 6 elements
/> describe ints
/ints is a list with 3 elements
/> cd ints
/ints> describe
/ints is a list with 3 elements
/ints> describe 0
/ints/0 is a int
/ints> 
```

### `pwd`
The `pwd` subcommand prompts the location of the current node - in a filesystem, you might think of this as the _current working directory_.  It's also part of each and every prompt but it's such a popular command and it was an easy thing to add so I added it. 

## Notes

- The tool leans heavily on the Python [`cmd` module](https://docs.python.org/3/library/cmd.html) and does the following:
  - Tab-completion for subcommand verbs and potential arguments
  - Command history:
    - History: Use the up and down arrows to go through subcommands previously issued
    - Editing: use the left and right arrows to move around a subcommand to make changes
- I have ideas for more subcommands:
  - Changing the JSON object:
    - Adding elements
    - Deleting elements
    - Changing element values
  - Writing out the object (the entire object or just from the current node)
  - Finding objects - I envision something like the Unix `find` command but geared toward `json-shell` and nodes
