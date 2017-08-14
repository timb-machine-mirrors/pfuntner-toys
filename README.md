<h1>Bruno's Toys</h1>

<p>These are scripts that I've found useful that I thought I would share with other folks.</p>
<p>I must admit that there are some tools in here I don't really expect others to make much use of.  Some are in here that are useful to me and I like to have them in the repo so I have a central place where I can store them in and where I can deploy them from easily.</p>

<table>
<tr><th>Script</th><th>Description</th><th>Example</th></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/banner">banner</a></td><td>This prints a message in a <span style="font-style: italic">banner</spam>.  I often use this inside scripts or in interactive loop as an <span style="font-style: italic">eye catcher</span></td><td><pre>
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

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/bashprofiles">bashprofiles</a></td><td>Most people know that <tt>bash</tt> supports a user profile but some people don't know that <tt>bash</tt> supports various file names and uses the first one that it finds in a defined order.  Personally, I can never remember all the file names exactly, don't remember the order they're used, and often can't remember the file used for a particular system.
<br/>
I've tried to simply the problem with this script.  By default, it will just tell you the profile <tt>bash</tt> will use for you, even if you have two or more to choose from.  One of my favorite ways to use the default behavior is to edit my profile file.  I don't care what the name is - just edit it!
<pre>
$ vi $(bashprofiles)
</pre>
<br/>
Alternatively, you can also have the script tell you which files you have, in the order that `bash` looks for them.</td><td><pre>
$ bashprofiles
/home/bruno/.profile
$ bashprofiles -v
You do not have /home/bruno/.bash_profile
You do not have /home/bruno/.bash_login
You have /home/bruno/.profile
$</pre></td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/beeper">beeper</a></td><td>This is a script that simply beeps forever - or at least until you kill it.  The way I use it is I combine it with another command that I expect to run for several seconds, it not several minutes.  <tt>beeper</tt> will let me know when the other command finishes.</td><td><pre>
$ date; sleep 5; date; beeper
Mon Aug 14 12:31:36 EDT 2017
Mon Aug 14 12:31:41 EDT 2017
***********************************************
* 2017-08-14 12:31:41.396286: Beeping started *
***********************************************
^C
*********************************************
* 2017-08-14 12:31:46.812411: Beeping ended *
*********************************************
$
</pre></td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/bingrep">bingrep</a></td><td>This is a script that searches arbitrary data for a regular expression.  Binary data won't disturb the search or the results!  Unprintable characters will be displayed by their hexcode.  Each hit is preceded by a number presenting the byte-position where the hit is found and 20 characters before and after the hit are included.</td><td><pre>
$ bingrep kill < /bin/bash
 75421 'nprintf_chk\x00strtoul\x00killpg\x00strcat\x00umask\x00strc'
 78947 'refixes\x00rl_backward_kill_word\x00rl_last_func\x00_'
 79154 'n_wc\x00reader_loop\x00rl_kill_region\x00rl_forward_b'
 81257 'pletion_matches\x00_rl_kill_kbd_macro\x00get_minus'
 83454 'rl_last_command_was_kill\x00find_user_command\x00s'
 84701 'pos\x00rl_set_retained_kills\x00phash_remove\x00_rl_p'
 84864 'ions\x00source_builtin\x00kill_all_local_variables'
 86279 'ariable\x00rl_backward_kill_line\x00word_token_ali'
 87696 'rl_find_next_mbchar\x00kill_current_pipeline\x00ev'
 88490 'ing\x00mail_warning\x00rl_kill_text\x00ifs_is_null\x00ar'
 90019 'l\x00rl_copy_keymap\x00rl_kill_line\x00rl_already_pro'
 90874 'ispose\x00strlist_walk\x00kill_doc\x00_rl_caught_sign'
 91557 '\x00_rl_overwrite_char\x00kill_pid\x00test_builtin\x00hi'
103880 'es\x00run_exit_trap\x00rl_kill_full_line\x00getopts_b'
106389 'r\x00rl_copy_region_to_kill\x00get_alias_value\x00rl_'
107103 'pletion_function\x00rl_kill_word\x00tilde_addition'
109888 'isearch_terminators\x00kill_builtin\x00rl_set_pare'
785015 'backward-word\x00shell-kill-word\x00shell-backward'
785040 'word\x00shell-backward-kill-word\x00history-and-al'
809631 ' to the shell with "kill -signal $$".\n    \n '
825119 'ows processes to be killed if the limit\n    '
845136 '[-ar] [jobspec ...]\x00kill [-s sigspec | -n si'
845198 'id | jobspec ... or kill -l [sigspec]\x00read ['
876095 'kward-char\x00backward-kill-line\x00beginning-of-h'
876288 'word\x00copy-region-as-kill\x00delete-char-or-list'
876672 '\x00insert-completions\x00kill-whole-line\x00kill-reg'
876688 'ons\x00kill-whole-line\x00kill-region\x00menu-complet'
$
</pre></td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/br">br</a></td><td>This is a script that you kind of have to use to appreciate.  It reads from stdin, stashes the data verbatim in a temporary file, launches <tt>vi</tt> on the file, and then removes the file when you're done.  So it's a little bit like <tt>more</tt> but I think it's much more flexible and you have a full editor to play with.
<br/>Alternatively, if you run it without redirecting stdin and give it one or more filenames, it launches <tt>vi</tt> in read-only mode.  I used to have a script for years that would only do <i>read-only</i> editing but I finally combined them together.</td><td>It's too interactive to give a good example.  Just try it out.</td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/columns">columns</a></td><td>I love this script so much!  I must use this at least an average of once a day!  The basic idea is that you tell it the positional columns you want to print and it prints them out.  Sounds easy, huh?  You can can specify columns in a few days:<ul>
<li>a single integer, the first column is <tt>1</tt></li>
<li>two integers separated by a hyphen - <tt>1-3</tt> is synonymous with <tt>1 2 3</tt></li>
<li>a single negative integer counts columns backwards - <tt>-1</tt> is the last column</tt></li>
</ul>Be aware that if the first column you specify is negative, you'll likely have to use a <em>trick</em> to make it so that the script will not think that <tt>-1</tt> is not supposed to be an option:

<pre>
$ columns -- -1
</pre>

This is a common technique when invoking Unix commands so it's handy to remember!
</td><td><pre>
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
$</pre></td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/cores">cores</a></td><td>Summarizes output from the Linux `lscpu` command.  I must confess that I don't often think of using this one but I probably need to get more into the habit of using it.  I'm not crazy about the name `cores` - I wonder if `cpus` would be easier for me to remember, etc.</td><td><pre>
$ cores
CPU(s): 4
Core(s) per socket: 2
8
$</pre></td></tr>

<tr><td><a href="https://github.com/pfuntner/toys/blob/master/git">git</a></td><td><p>No, I didn't re-write <tt>git</tt>!!  This is a front-end to <tt>/usr/bin/git</tt> which supplies my github user & token for prompts.  I created this because of I got sick of having to enter the token myself.  Also, I have to have the presence of mine to <b>get</b> my token every time!  I have it stored in a file in my home directory but I had to cat it every time I wanted to use a <tt>git</tt> command!  This solves the problem <b>for the most part</b>  I usually have a copy of the script and the associated JSON file in my bin directory.  Instead of putting <tt>$HOME/bin</tt> early in my <tt>$PATH</tt>, I usually just create a shell alias for <tt>git</tt> which leads to my script.</p>
<p>The script is not perfect!  There are some instances where <tt>git</tt> wants to do something interactively with me and the script just hangs because it doesn't expect such a prompt.  Often, there isn't even any warning before the hang.  If I get the sense that the script is hanging, I have to cancel it, get my token, and re-issue the command with an absolute path to <tt>/usr/bin/git</tt> to see what it was really doing.</td><td>There isn't much to show.  Just use the script as a substitute for <tt>git</tt>.</td></tr>
<tr><td><a href="https://github.com/pfuntner/toys/blob/master/seejson">seejson</a></td><td>A ridiculously simple Python script that takes JSON written in an arbitrary way and prints it out in a pretty from.  I say it's simple because it's just using the Python JSON module to do most of the work.  The result is great!</td><td>
<pre>
$ echo '{"one": 1, "two": [2] }' | seejson
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
