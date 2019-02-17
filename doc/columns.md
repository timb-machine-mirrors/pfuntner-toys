<h1><tt>columns</tt><h1>

<h2>Purpose</h2>
<p>I love this script so much! I must use this at least an average of once a day! The basic idea is that you tell it the positional columns you want to print and it prints them out.</p>
<h2>Syntax</h2>
<pre>
Syntax: columns [-F CHAR] [--regexp REGEXP] [col] [-col1] [col1-col2]
</pre>

<h3>Options and arguments</h3>
<table>
<tr>
<th>Option</th><th>Description</th><th>Default</th>
</tr>
<tr>
<td><tt>-F</tt></td><td>Specifies the character by which to break up tokens</td><td>The default is to parse tokens by spaces</td>
</tr>
<tr>
<td><tt>--regexp</tt></td><td>Specifies a regular expression by which to break up tokens</td><td>The default is to parse tokens by spaces</td>
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
<li>Since creating this script, I learned about the <a href="http://man7.org/linux/man-pages/man1/column.1.html"><tt>column</tt></a> command common on Linux systems (although it's not part of the <a href="http://pubs.opengroup.org/onlinepubs/7908799/"><i>Single Unix Specification</i></a>), which is kind of similar.  My script has some more features in formatting but <tt>column</tt> might be a good alternative too.</li>
</ul>
