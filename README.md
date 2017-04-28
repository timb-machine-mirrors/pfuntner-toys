# Bruno's Toys

<p>These are scripts that I've found useful that I thought I would share with other folks.</p>
<p>I must admit that there are some tools in here I don't really expect others to make much use of.  Some are in here that are useful to me and I like to have them in the repo so I have a central place where I can store them in and where I can deploy them from easily.</p>

<table>
<tr><th>Script</th><th>Description</th><th>Example</th></tr>

<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/banner">banner</a></td><td>This prints a message in a <span style="font-style: italic">banner</spam>.  I often use this inside scripts or in interactive loop as an <span style="font-style: italic">eye catcher</span></td><td><pre>
$ banner hello
#########
# hello #
#########
$ (echo "The time is"; date) | banner --center -c '*'
********************************
*         The time is          *
* Fri Apr 28 09:51:15 EDT 2017 *
********************************
$
</pre></td></tr>

<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/bashprofiles">bashprofiles</a></td><td>Most people know that `bash` supports a user profile but some people don't know that `bash` supports various file names and uses the first one that it finds in a defined order.  Personally, I can never remember all the file names exactly, don't remember the order they're used, and often can't remember the file used for a particular system.
<br/>
I've tried to simply the problem with this script.  By default, it will just tell you the profile `bash` will use for you, even if you have two or more to choose from.  One of my favorite ways to use the default behavior is to edit my profile file.  I don't care what the name is - just edit it!
<pre>
$ vi $(bashprofiles)
</pre>
<br/>
Alternatively, you can also have the script tell you which files you have, in the order that `bash` looks for them.</td><td><pre>
$ bashprofiles
/home/ibmadmin/.profile
$ bashprofiles -v
You do not have /home/ibmadmin/.bash_profile
You do not have /home/ibmadmin/.bash_login
You have /home/ibmadmin/.profile
$</pre></td></tr>

<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/browser">browser</a></td><td>This is a script that you kind of have to use to appreciate.  It reads from stdin, stashes the data verbatim in a temporary file, launches `vi` on the file, and then removes the file when you're done.  So it's a little bit like `more` but I think it's much more flexible and you have a full editor to play with.</td><td>It's too interactive to give a good example.  Just try it out.</td></tr>

<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/git">git</a></td><td><p>No, I didn't re-write <tt>git</tt>!!  This is a front-end to <tt>/usr/bin/git</tt> which supplies my github user & token for prompts.  I created this because of I got sick of having to enter the token myself.  Also, I have to have the presence of mine to <b>get</b> my token every time!  I have it stored in a file in my home directory but I had to cat it every time I wanted to use a <tt>git</tt> command!  This solves the problem <b>for the most part</b>  I usually have a copy of the script and the associated JSON file in my bin directory.  Instead of putting <tt>$HOME/bin</tt> early in my <tt>$PATH</tt>, I usually just create a shell alias for <tt>git</tt> which leads to my script.</p>
<p>The script is not perfect!  There are some instances where <tt>git</tt> wants to do something interactively with me and the script just hangs because it doesn't expect such a prompt.  Often, there isn't even any warning before the hang.  If I get the sense that the script is hanging, I have to cancel it, get my token, and re-issue the command with an absolute path to <tt>/usr/bin/git</tt> to see what it was really doing.</td><td>There isn't much to show.  Just use the script as a substitute for <tt>git</tt>.</td></tr>
<tr><td><a href="https://github.ibm.com/pfuntner/toys/blob/master/seejson">seejson</a></td><td>A ridiculously simple Python script that takes JSON written in an arbitrary way and prints it out in a pretty from.  I say it's simple because it's just using the Python JSON module to do most of the work.  The result is great!</td><td>
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
