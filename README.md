# Bruno's Toys

These are scripts that I've found useful that I thought I would share with other folks.

<table>
<tr><th>Script</th><th>Description</th><th>Example</th></tr>
<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/git">git</a></td><td><p>No, I didn't re-write <tt>git</tt>!!  This is a front-end to <tt>/usr/bin/git</tt> which supplies my github user & token for prompts.  I created this because of I got sick of having to enter the token myself.  Also, I have to have the presence of mine to <b>get</b> my token every time!  I have it stored in a file in my home directory but I had to cat it every time I wanted to use a <tt>git</tt> command!  This solves the problem <b>for the most part</b>  I usually have a copy of the script and the associated JSON file in my bin directory.  Instead of putting <tt>$HOME/bin</tt> early in my <tt>$PATH</tt>, I usually just create a shell alias for <tt>git</tt> which leads to my script.</p>
<p>The script is not perfect!  There are some instances where <tt>git</tt> wants to do something interactively with me and the script just hangs because it doesn't expect such a prompt.  Often, there isn't even any warning before the hang.  If I get the sense that the script is hanging, I have to cancel it, get my token, and re-issue the command with an absolute path to <tt>/usr/bin/git</tt> to see what it was really doing.</td><td>There isn't much to show.  Just use the script as a substitute for <tt>git</tt>.</td></tr>
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
