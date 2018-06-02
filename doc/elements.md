# `elements`

## Purpose
Takes a JSON list of dictionaries and prints keys of the elements in tabular form.

## Syntax
```
Syntax:
  elements -a
  elements --all
  elements FIELD ...
  elements -h
  elements --help
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-a` or `-all`  | Includes all keys of the first dictionary | Not enabled |
| `-h` or `--help` | Prints the keys of the first dictionary.  Useful to form custom commands. | See the notes |

## Example

```
$ Data.py getListOfDicts | elements --all
hvesxfuobhxatl|anslrihhwxicwd|zeppbteo                            |kzzfkiprywohkx|mulls|olcniuqs      |pkeyk
True          |    2124568168|fe7f5aee-a1fc-4cdf-963d-229b6cc5260b| 2102841335.02|True |hwjvu         |0171-06-07 23:01:28.393000
True          |    1298911667|623fe182-10a2-4168-b3b4-f7978e512253| 1958123208.02|False|zourkzdbrptyfj|1493-03-14 22:03:29.468002
True          |   -1296010529|32a1703d-d997-41ca-8b48-34bde5e1a088|-775493326.306|True |dcewyzsunddvfy|1260-04-07 05:50:07.953003
True          |    -781779455|d3a17a82-c193-4219-b59d-b027e61b0d24|-2136559919.05|False|gzafhev       |2080-07-11 18:25:00.536003
False         |    -348973581|a7ac81ba-7201-4428-99db-15875ac15aba| 2036871096.45|True |mdwerhrzt     |0610-12-18 14:01:05.303001
True          |   -1729085288|22b0a1df-6b8f-42ac-b4f3-1956e94075bb|-31867464.9191|False|pxicgpilkwhwb |0082-01-30 02:29:02.719000
False         |    2134320521|b7ee14f2-53c5-4207-8a87-c8aa746671c1| 2048902606.01|False|jlhdvqdkvvtwx |2319-10-31 11:49:12.871002
False         |      93616471|73915a00-f3dc-44bc-b7d9-96346c1e7d16| 574805680.655|True |csqlznt       |0175-10-12 22:49:33.651000
```

```
$ Data.py getListOfDicts > /tmp/random.json
$ elements --help < /tmp/random.json
Fields are: amtzkpjmbrols, byteoqsex, gmakptsmmolbew, huftweutebvid, lsyosvikeqchob, lwhmyqurugd, mxivxhistuqjx, pkwlgnshnlgmy, plbjzlnq, whhx
$ elements whhx plbjzlnq < /tmp/random.json
whhx                      |plbjzlnq
2372-02-05 21:40:58.509995|948170f8-d544-40bc-b90d-1952d3ea33cb
1960-08-17 17:16:50.778999|0a11e942-6306-4591-bf33-3cf1165d4514
0263-04-16 08:10:04.371000|27310623-088a-44f6-ba94-3dfbc2b73a14
1149-08-27 22:08:21.266998|33e50693-d06e-43f5-8cd8-5e5dc1372a03
2115-10-27 02:58:47.524002|092e5537-b041-4cd8-82e8-2a72191986cd
$ 
```

## Notes

- The tool only reads data from stdin.
- The data **must** be a list of dictionaries:
  ```
  [
    { "key1": "element 1, value1", "key2": "element 1, value2", ... },
    { "key1": "element 2, value1", "key2": "element 2, value2", ... },
    .
    .
    .
  ]
  ```
- The available fields are based upon the fields in the first element.
- Remember that when using the `-all` option, the available keys are based on the **first** element.  This means:
  - If a key from the first element is not in another element, the value of the key for that element is `n/a`
  - If a key from an element other than the first element does not appear in the first element, it will not be printed.
- If you do not supply any options or fields but you supply a valid JSON object through stdin:
  - A syntax message will remind you of the syntax of the command
  - A message will display the available keys of the first element (see the `--help` option).
- Originally, I stared writing this tool to process data from a private tool of mine _(maybe I'll make it available **some day**)_ - it continually pings a remote host to see if it's alive and the network connection is working.  I created the private tool because my sucky ISP at home (I don't mind calling them out it's **Time Warner / RoadRunner / Spectrum /** whatever!) often drops me and I wanted to monitor the situation.  Anyway, halfway through writing what _became_ `elements`, I thought:
  
  > Hey, other people mightappreciate this tool!
  
  Honestly, that's how many of my tools begin!!
- The examples make use of my `Data.py` class/command.  I actually wrote it **because** I wanted something to generate random data for the examples for `elements`!