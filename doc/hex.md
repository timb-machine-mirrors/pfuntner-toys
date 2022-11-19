# `hex`

## Purpose
Print out a file or data in hexadecimal and character form

## Syntax
```
Syntax: hex [-8] [file ...]
```

### Options and arguments
| Option | Description | Default |
| ------ | ----------- | ------- |
|  `-8`  | Display eight bytes per line | Sixteen bytes are printed on each line |

## Examples

### Reading a file
```
$ cat /etc/motd
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Welcome to bruno-meerkat ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
$ hex /etc/motd
00000000 \xe2 \x94 \x8f \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2
           e2   94   8f   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2
00000010 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94
           94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94
00000020 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81
           81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81
00000030 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2
           e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2
00000040 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94
           94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94
00000050 \x81 \xe2 \x94 \x93   \n \xe2 \x94 \x83         W    e    l    c    o    m    e
           81   e2   94   93   0a   e2   94   83   20   57   65   6c   63   6f   6d   65
00000060         t    o         b    r    u    n    o    -    m    e    e    r    k    a
           20   74   6f   20   62   72   75   6e   6f   2d   6d   65   65   72   6b   61
00000070    t      \xe2 \x94 \x83   \n \xe2 \x94 \x97 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2
           74   20   e2   94   83   0a   e2   94   97   e2   94   81   e2   94   81   e2
00000080 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94
           94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94
00000090 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81
           81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81
000000a0 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2
           e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2
000000b0 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94
           94   81   e2   94   81   e2   94   81   e2   94   81   e2   94   81   e2   94
000000c0 \x81 \xe2 \x94 \x81 \xe2 \x94 \x81 \xe2 \x94 \x9b   \n
           81   e2   94   81   e2   94   81   e2   94   9b   0a
```

### Reading data from stdin
```
$ head -8 -c40 /dev/urandom | hex
00000000 \xa3 \x82 \xf5   \n    b \xd2    l \x96 \x98 \xb0 \xac    U \x9c    b    Q \xc4
           a3   82   f5   0a   62   d2   6c   96   98   b0   ac   55   9c   62   51   c4
00000010 \xdb \x81    + \xe9 \x11 \x05 \xec \xc3    8 \xa6 \x1c    !    (    o \xd7    I
           db   81   2b   e9   11   05   ec   c3   38   a6   1c   21   28   6f   d7   49
00000020 \x07 \xa2 \xa2 \x12    | \x88 \x01 \xc8
           07   a2   a2   12   7c   88   01   c8
$
```

### All characters!
```
$ peval '"".join([chr(num) for num in range(256)])' | hex
00000000 \x00 \x01 \x02 \x03 \x04 \x05 \x06 \x07 \x08   \t   \n \x0b \x0c   \r \x0e \x0f
           00   01   02   03   04   05   06   07   08   09   0a   0b   0c   0d   0e   0f
00000010 \x10 \x11 \x12 \x13 \x14 \x15 \x16 \x17 \x18 \x19 \x1a \x1b \x1c \x1d \x1e \x1f
           10   11   12   13   14   15   16   17   18   19   1a   1b   1c   1d   1e   1f
00000020         !    "    #    $    %    &    '    (    )    *    +    ,    -    .    /
           20   21   22   23   24   25   26   27   28   29   2a   2b   2c   2d   2e   2f
00000030    0    1    2    3    4    5    6    7    8    9    :    ;    <    =    >    ?
           30   31   32   33   34   35   36   37   38   39   3a   3b   3c   3d   3e   3f
00000040    @    A    B    C    D    E    F    G    H    I    J    K    L    M    N    O
           40   41   42   43   44   45   46   47   48   49   4a   4b   4c   4d   4e   4f
00000050    P    Q    R    S    T    U    V    W    X    Y    Z    [   \\    ]    ^    _
           50   51   52   53   54   55   56   57   58   59   5a   5b   5c   5d   5e   5f
00000060    `    a    b    c    d    e    f    g    h    i    j    k    l    m    n    o
           60   61   62   63   64   65   66   67   68   69   6a   6b   6c   6d   6e   6f
00000070    p    q    r    s    t    u    v    w    x    y    z    {    |    }    ~ \x7f
           70   71   72   73   74   75   76   77   78   79   7a   7b   7c   7d   7e   7f
00000080 \x80 \x81 \x82 \x83 \x84 \x85 \x86 \x87 \x88 \x89 \x8a \x8b \x8c \x8d \x8e \x8f
           80   81   82   83   84   85   86   87   88   89   8a   8b   8c   8d   8e   8f
00000090 \x90 \x91 \x92 \x93 \x94 \x95 \x96 \x97 \x98 \x99 \x9a \x9b \x9c \x9d \x9e \x9f
           90   91   92   93   94   95   96   97   98   99   9a   9b   9c   9d   9e   9f
000000a0 \xa0 \xa1 \xa2 \xa3 \xa4 \xa5 \xa6 \xa7 \xa8 \xa9 \xaa \xab \xac \xad \xae \xaf
           a0   a1   a2   a3   a4   a5   a6   a7   a8   a9   aa   ab   ac   ad   ae   af
000000b0 \xb0 \xb1 \xb2 \xb3 \xb4 \xb5 \xb6 \xb7 \xb8 \xb9 \xba \xbb \xbc \xbd \xbe \xbf
           b0   b1   b2   b3   b4   b5   b6   b7   b8   b9   ba   bb   bc   bd   be   bf
000000c0 \xc0 \xc1 \xc2 \xc3 \xc4 \xc5 \xc6 \xc7 \xc8 \xc9 \xca \xcb \xcc \xcd \xce \xcf
           c0   c1   c2   c3   c4   c5   c6   c7   c8   c9   ca   cb   cc   cd   ce   cf
000000d0 \xd0 \xd1 \xd2 \xd3 \xd4 \xd5 \xd6 \xd7 \xd8 \xd9 \xda \xdb \xdc \xdd \xde \xdf
           d0   d1   d2   d3   d4   d5   d6   d7   d8   d9   da   db   dc   dd   de   df
000000e0 \xe0 \xe1 \xe2 \xe3 \xe4 \xe5 \xe6 \xe7 \xe8 \xe9 \xea \xeb \xec \xed \xee \xef
           e0   e1   e2   e3   e4   e5   e6   e7   e8   e9   ea   eb   ec   ed   ee   ef
000000f0 \xf0 \xf1 \xf2 \xf3 \xf4 \xf5 \xf6 \xf7 \xf8 \xf9 \xfa \xfb \xfc \xfd \xfe \xff
           f0   f1   f2   f3   f4   f5   f6   f7   f8   f9   fa   fb   fc   fd   fe   ff
00000100   \n
           0a
$
```
This last example uses my [`peval`](peval.md) tool.

## Notes

- Traditionally, I use the Unix [`od`](http://pubs.opengroup.org/onlinepubs/7908799/xcu/od.html) command to show files like this but the incantation can be cryptic and inconsistent
  - Usually on Linux, I would use `od -ctx1` but that's quite cryptic.  I honestly can't even tell you what each option means from memory.
    - I think I tried to have someone try this on their Mac laptop and it wasn't working.
  - Many years ago (maybe in my days with [IBM z/OS](https://www.wikiwand.com/en/Z/OS)), I think I got use to use `od -ch` or something like that.  It's been so long that I can't remember clearly.
- The character form is a _best effort_ courtesy of the Python _repr()_ function:
  - Regular characters (letters, digits, punctuation, space) are displayed as is
  - Other whitespace characters (excluding spaces) are printed with as a _simple common escape_ such as `\n` for a newline
  - Otherwise, the character is shows in hex form
