# Bruno's Toys

These are scripts that I've found useful that I thought I would share with other folks.

<table>
<tr><th>Script</th><th>Description</th><th>Example</th></tr>
<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/seejson">json</a></td><td>A ridiculously simple Python script that takes JSON written in an arbitrary way and prints it out in a pretty from.  I say it's simple because it's just using the Python JSON module to do most of the work.  The result is great!</td><td>
<pre>
$ echo '{"one": 1, "two": [2] }' \| seejson
{
  "two": [
    2
  ],
  "one": 1
}
$
</pre>
</td></tr>
</table>
