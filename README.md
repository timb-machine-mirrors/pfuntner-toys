# Bruno's Toys
This is a collection of Unix tools command line that make my life easier.  I think others might like them too so I'm making them available here but the repository is just a nice way for me to keep track of changes and deploy them easily to systems.

I will admit that the documentation is rather poor for some of the tools and many of them have little or **no** comments.  This is a work in progress - I'm constantly creating new tools and improving documentation.  In November 2017, I did a major overhaul of the documentation because I was disatisfed with having a huge table.  I'm liking the results so far.

If you have questions, problems, etc, you can reach me at <img src="images/email.jpg" />.

### Unix platforms

Over the years, I've used many different _Unix_ platforms: Redhat, Suse, Solaris, HP/UX, AIX, Z/OS, Cygwin, Git bash, etc.  I owe no allegiance to any single platform and consider them all pretty much equal as long as they behave similarly.  I have seen some issues using my tools (and other commands!) from Git bash on Windoze and sometimes a tool was only designed to work on specific platforms - I'll try to put such stuff on the doc page for the tool.  In general if I find a platform where one of my tools doesn't work well, I will try to fix it!

## The much-heralded TOOLS

Select a tool below to learn more about it.  The _Bruno's Favorite_ column is used to indicate that a tool is:
- very useful and practical
- personally used by me a few times a week if not at least once a day!
- I thought about expressing an extreme affection for some tools but realized I might be expressing it for all of the favorites so I'll just leave it as _favorite_ or _not favorite_

| Tool | Bruno's Favorite? | Brief Description |
| ---- | ----------------- | ----------------- |
| [`banner`](doc/banner.md) | Yes | Prints text in a _banner_ |
| [`bashprofiles`](doc/bashprofiles.md) | | Prints profile script(s) `bash` will use |
| [`beeper`](doc/beeper.md) | | Beeps over and over |
| [`bingrep`](doc/bingrep.md) | | Searches for a regular expression in arbitrary data from stdin |
| [`br`](doc/br.md) | Yes | Browse a file.  Sounds simple?  Maybe, but give it a try |
| [`capture`](doc/capture.md) | | Saves output and other information from a command |
| [`columns`](doc/columns.md) | Yes | Prints _columns_ of stdin where columns are separated by a character or regular expression |
| [`comm2`](doc/comm2.md) | | Alternate version of `comm` that does not expect the data to be sorted |
| [`cores`](doc/cores.md) | | Prints CPU core information in a simple way |
| [`datemath`](doc/datemath.md) | | Perform arithmetic on date(s) |
| [`dowhile`](doc/dowhile.md) | | Perform a command repeatedly until output is seen in the output |
| [`extensions`](doc/extensions.md) | | Show extensions used by files |
| [`drop`](doc/drop.md) | Yes | Drop the first or last `n` lines, similar to `head`/`tail` |
| [`fernet`](doc/fernet.md) | | Perform fernet encryption/decryption |
| [`flow`](doc/flow.md) | Yes | Flow lines from stdin into columnar form |
| [`gitstatus`](doc/gitstatus.md) | | Show files in a local git repo that have been changed, etc. |
| [`headtail`](doc/headtail.md) | Yes | Print out the top and bottom of stdin or one or more files |
| [`json`](doc/json.md) | Yes | JSON magic - it's a disservice to try to summarize this tool in a single string. |
| [`megadiff`](doc/megadiff.md) | | Compare two directories trees |
| [`peval`](doc/peval.md) | Yes | Evaluate Python expression strings |
| [`pycomment`](doc/pycomment.md) | | vi command to toggle Python-style comments, similar to PyCharm `ctrl-/` command |
| [`SecureKeyValues`](doc/SecureKeyValues.md) | | Manage secure key value stores |
| [`timer`](doc/timer.md) | | Display a progress meter over a specified duration of time |
| [`timestamps`](doc/timestamps.md) | | Show times when files were last modified, most-recently updated first |
| [`uniqc`](doc/uniqc.md) | Yes | Counts unique instances of input |
| [`undupe`](doc/undupe.md) | | Removes duplicate punctuation & whitespace |
| [`unixdate`](doc/unixdate.md) | | Invokes `date` with Unix-style format on Windoze |
