# `Data.py`

## Purpose
Generates random data for various purposes:
- testing
- demonstrations/examples
- more??


## Syntax
```
Syntax: Data.py [getBoolean|getDatetime|getInteger|getName|getNumber|getUuid|getListOfDicts]
```

  | Argument | Description |
  | ------- | ----------- |
  | `getBooleans` | A boolean value (`True` or `False`)|
  | `getDatetimes` | A [`datetime`](https://docs.python.org/2/library/datetime.html#datetime-objects) which could range from 0001/01/01 through 2500/01/01 |
  | `getIntegers` | An integer from 0 to 2\*\*32 |
  | `getNames` | A string which is composed of four to sixteen lowercase letters |
  | `getNumbers` | A real number from -(2\*\*32) to (2\*\*32)|
  | `getUuids` | A random [UUIDs](https://docs.python.org/2/library/uuid.html#uuid.uuid4) |
  | `getListOfDicts` | A JSON list of dictionaries with a random set of keys, cycling through the different data types known by the tool. |

### Options and arguments
None

## Examples

```
$ Data.py | json
{
  "booleans": [
    false,
    false,
    true,
    false,
    false,
    false,
    true,
    false,
    true,
    false
  ],
  "dates": [
    "1720-05-08T05:54:02.862999",
    "1164-02-02T13:54:30.566002",
    "2471-12-15T03:40:31.026001",
    "0006-10-18T20:35:09.877000",
    "0610-05-04T08:27:02.567001",
    "0102-07-31T16:46:36.450000",
    "0417-11-11T05:15:29.693001",
    "1488-10-20T15:58:56.084999",
    "2034-09-15T12:14:02.912003",
    "0476-12-12T12:53:42.820000"
  ],
  "integers": [
    1104504202,
    -1826536329,
    177193775,
    1710265524,
    937586827,
    854293851,
    880000303,
    -1770627169,
    1275419393,
    1495530997
  ],
  "listOfDicts": [
    {
      "ergzgpwrfwajdi": "False",
      "ibjw": "-2020758106",
      "lcceu": "4cf34527-56b6-4734-b11b-1d69bd45a86b",
      "nhhxndgfki": "False",
      "vucobq": "0731-02-06 09:33:46.841999",
      "vxuogbdo": "pyseu",
      "xbbiwnwzmelw": "57600712.9351"
    },
    {
      "ergzgpwrfwajdi": "False",
      "ibjw": "1698710362",
      "lcceu": "9feae2ef-faca-4cd2-a64e-5cc4085b1a7b",
      "nhhxndgfki": "True",
      "vucobq": "0417-11-27 21:42:21.495001",
      "vxuogbdo": "nzlkq",
      "xbbiwnwzmelw": "16973348.6136"
    },
    {
      "ergzgpwrfwajdi": "True",
      "ibjw": "1495571553",
      "lcceu": "557e1350-1800-4c01-9a13-7aefc36ffd75",
      "nhhxndgfki": "True",
      "vucobq": "1194-02-02 21:57:44.054001",
      "vxuogbdo": "napseefby",
      "xbbiwnwzmelw": "-958823552.313"
    },
    {
      "ergzgpwrfwajdi": "False",
      "ibjw": "1473114499",
      "lcceu": "7028949d-dfb7-48d8-a39d-7716362af93b",
      "nhhxndgfki": "True",
      "vucobq": "0903-09-22 03:32:14.953999",
      "vxuogbdo": "sxaspkwxfmrmb",
      "xbbiwnwzmelw": "-453617011.318"
    }
  ],
  "names": [
    "uljzvtxl",
    "vmqvuvgzm",
    "qmiubeoausbdu",
    "nepvtrwzxcyt",
    "ikbtieqftkckx",
    "uihsveamlh",
    "eyee",
    "ifsixoqbvrnba",
    "aapuraogyx",
    "tujxrt"
  ],
  "numbers": [
    -1359542513.9570265,
    1197774661.6605911,
    -1973813696.466072,
    125408289.81624317,
    -896152972.4880755,
    -706209415.4888449,
    -861945234.3999388,
    53419925.61462307,
    813787450.3756728,
    -1888716731.2101645
  ],
  "uids": [
    "eaa4fb0f-f21f-4d6f-b2c2-b21e98d9c835",
    "d101d994-0ec5-4b83-8b18-5e1e2d617881",
    "cb4d890c-6613-4aaf-a99b-b0a64eb0fb28",
    "74e1f11f-8d55-4ad7-af8b-af3597f5a020",
    "f9d28cdc-28c2-4bbe-8eba-a03c1a066501",
    "6762b7c9-2445-46a7-ab0c-161e9bbf1c4e",
    "e16a8b7f-2ea9-43f7-a708-db6a95657d01",
    "648d17bc-f36b-41f5-a60c-6684cba21264",
    "d00a0508-0e59-4fe1-bb47-800f7fa35e34",
    "c3c964a8-64a6-43d3-b30f-202fb8c1277c"
  ]
}
```
```
$ Data.py getListOfDicts | json
[
  {
    "diqs": "False",
    "kooptsdtnlhlw": "-638191135",
    "ljtp": "1705435881.34",
    "qubehinfmdlnmcwd": "True",
    "rhecnrb": "7c4d8c4d-246b-4b98-a416-b3a52517961a",
    "uuxskzpcp": "mkycwexzykshb",
    "ypkcvcsicxbq": "2338-07-19 17:53:37.313995"
  },
  {
    "diqs": "False",
    "kooptsdtnlhlw": "1153523069",
    "ljtp": "956891997.446",
    "qubehinfmdlnmcwd": "False",
    "rhecnrb": "d5be5d1b-2f0a-403b-b47e-083e5d1bd33e",
    "uuxskzpcp": "mrcnm",
    "ypkcvcsicxbq": "0903-07-03 15:39:44.339001"
  },
  {
    "diqs": "True",
    "kooptsdtnlhlw": "-960024089",
    "ljtp": "775161287.967",
    "qubehinfmdlnmcwd": "False",
    "rhecnrb": "64d3ba95-527d-47b8-8382-877af1d250f2",
    "uuxskzpcp": "ulzboexpcxebshl",
    "ypkcvcsicxbq": "1568-06-19 23:58:49.760002"
  },
  {
    "diqs": "True",
    "kooptsdtnlhlw": "-2059724666",
    "ljtp": "1710360439.37",
    "qubehinfmdlnmcwd": "False",
    "rhecnrb": "533fa03c-a483-4703-a501-ccf3e869d8c6",
    "uuxskzpcp": "nqti",
    "ypkcvcsicxbq": "2156-04-25 13:14:04.829002"
  },
  {
    "diqs": "False",
    "kooptsdtnlhlw": "621319692",
    "ljtp": "-735137015.592",
    "qubehinfmdlnmcwd": "False",
    "rhecnrb": "ea28083d-addd-49b4-bf6d-5e535e80ee33",
    "uuxskzpcp": "muffipvkeho",
    "ypkcvcsicxbq": "1956-07-13 11:46:16.015999"
  }
]
$
```

## Notes

- The tool is designed to be used from the command line or inside another Python script:
  ```python
   from Data import Data
   .
   .
   .
   data = Data()
   listOfDicts = data.getListOfDicts()
  ```
- When used from the command line without an argument, a special JSON list of dictionaries are printed.  The `listOfDicts` element contains a JSON structure like `Data.py getListOfDicts` would return.  Additionally, there is an element for each of the other possible arguments with ten random values of that type - for instance, the `integer` element has a list of ten random integers (`Data.py getInteger`).
- The tool/class imports my [`table.py`](table.py.md) class - _Sorry if the doc for it doesn't exist yet but I hope to get to it someday!_  Anyway, you'll need that class to make use of this tool/class. It's only used when you use `Data.py` as a command maybe I could work around that but I haven't yet.
- The examples make use of my [`json`](json.md) tool.
