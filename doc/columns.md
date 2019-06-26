<h1><tt>columns</tt><h1>

<h2>Purpose</h2>
<p>I love this script so much! I must use this at least an average of once a day! The basic idea is that you tell it the positional columns you want to print and it prints them out.</p>
<h2>Syntax</h2>
<pre>
columns [-h] [-s DELIM | -r REGEXP | -c] [-n] [-f FILENAME] [-v] column [column ...]
</pre>

<h3>Options and arguments</h3>
<table>
<tr>
<th>Option</th><th>Description</th><th>Default</th>
</tr>
<tr>
<td><tt>-s DELIM</tt> or <tt>-F DELIM</tt> or <tt>--separator DELIM</tt> or <tt>--delim DELIM</tt></td><td>Specifies the regular expression to separate columns.</td><td>The default is to separate columns by one or more whitespace characters</td>
</tr>
<tr>
<td><tt>-r REGEXP</tt> or <tt>--regexp REGEXP</tt></td><td>Specifies a regular expression by which to break up tokens</td><td>The default is to separate columns by one or more whitespace characters</td>
</tr>
<tr>
<td><tt>-c</tt> or <tt>--csv</tt></td><td>Reads input as CSV</td><td>The default is to separate columns by one or more whitespace characters</td>
</tr>
<tr>
<td><tt>-n</tt> or <tt>--negate</tt></td><td>Excludes specified columns</td><td>Includes specified columns</td>
</tr>
<tr>
<td><tt>-f FILENAME</tt> or <tt>--filename FILENAME</tt></td><td>Reads input from the specified file</td><td>The default is to read from stdin</td>
</tr>
<tr>
<td><tt>-v</tt> or <tt>--verbose</tt></td><td>Enables debugging messages</td><td>Debugging messages are not printed</td>
</tr>
</table>
<p>
You can can specify columns in a few ways:
<ul>
<li>a single integer, the first column is 1</li>
<li>two integers separated by a hyphen - <tt>1-3</tt> is synonymous with <tt>1 2 3</tt>
<li>a single negative integer counts columns backwards - <tt>-1</tt> is the last column
</p>
<p>
Be aware that if the first column you specify is negative, you'll likely have to use a trick to make it so that the script will not think that <tt>-1</tt> is an option:
<pre>
$ columns -- -1
</pre>
This is a common technique when invoking Unix commands so it's handy to remember!
</p>
</ul>

<h2>Example</h2>
<pre>
$ ls -l
total 0
-rw-rw-r-- 1 bruno bruno 0 Aug 14 12:44 1
-r--r--r-- 1 bruno bruno 0 Aug 14 12:44 2
-rw-rw-r-- 1 bruno bruno 0 Aug 14 12:44 3
-rwxrwxr-x 1 bruno bruno 0 Aug 14 12:44 foobar.txt
$ ls -l | columns 1 -1
total 0
-rw-rw-r-- 1
-r--r--r-- 2
-rw-rw-r-- 3
-rwxrwxr-x foobar.txt
$
</pre>

<h2>Notes</h2>

<ul>
<li>The data is read from stdin.  If stdin is not directed from a file or pipe, en error message is printed and the script terminates</li>
<li>Negative columns don't work when `--negate` is specified and no error is thrown.</li>
</ul>
