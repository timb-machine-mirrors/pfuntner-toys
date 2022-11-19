# `bingrep`

## Purpose
This is a script that searches arbitrary data for a regular expression. Binary data won't disturb the search or the results! Unprintable characters will be displayed by their hexcode. Each hit is preceded by a number presenting the byte-position where the hit is found and 20 characters before and after the hit are included.

## Syntax
```
Syntax: bingrep REGEXP
```

### Options and arguments
There are no options supported.  The only argument is a regular expression.

## Example

```
$ bingrep jobs < /bin/bash
 79195 '_argument\x00count_all_jobs\x00command_word_comple'
 79319 'ning_trap\x00break_doc\x00jobs_doc\x00dirspell\x00coproc'
 83707 'odcase\x00list_stopped_jobs\x00string_list_dollar_'
 87290 'r\x00terminate_stopped_jobs\x00_rl_term_forward_ch'
 87548 'urcs\x00ttnocanon\x00sh_nojobs\x00until_doc\x00set_pwd\x00f'
 88327 'gin\x00return_catch\x00it_jobs\x00array_quote\x00netopen'
 96573 'vel_string\x00list_all_jobs\x00enable_builtin\x00_IO_'
 98215 'ch_history\x00unfreeze_jobs_list\x00ifs_firstchar\x00'
 99347 'r\x00parser_save_alias\x00jobs_builtin\x00file_isdir\x00'
 99842 'nd_chars\x00delete_all_jobs\x00current_command_sub'
101499 'f_char\x00list_running_jobs\x00let_builtin\x00type_do'
101774 'che\x00assoc_to_string\x00jobs_m_flag\x00pop_stream\x00i'
103157 'rectories\x00nohup_all_jobs\x00reading_shell_scrip'
104321 'user_info\x00reap_dead_jobs\x00rl_executing_macro\x00'
109506 'nd_array_list\x00check_jobs_at_exit\x00_rl_move_ve'
110064 '_changed\x00hangup_all_jobs\x00find_flag\x00executing'
839742 '\xf7\xff.././flags.c\x00.././jobs.c\x00<unknown>\x00Signal '
857874 'ently\n    \t\tstopped jobs.  If found there, t'
858034 'the list of stopped jobs.  A\n    \t\tvalue of '
885847 'r occurs.\x00\x00\x00\x00Remove jobs from current shell.'
885936 'the table of active jobs.  Without\n    any J'
886053 '      -a\tremove all jobs if JOBSPEC is not s'
886216 'remove only running jobs\n    \n    Exit Statu'
886330 '\x00\x00Display status of jobs.\n    \n    Lists the'
886362 '   Lists the active jobs.  JOBSPEC restricts'
886453 'tatus of all active jobs is displayed.\n    \n'
886712 't output to running jobs\n      -s\trestrict o'
886753 't output to stopped jobs\n    \n    If -x is s'
889781 ' is given.\x00\x00\x00\x00\x00Move jobs to the background.\n'
889824 '\n    \n    Place the jobs identified by each '
905624 '-ps arg [arg...]\x00\x00\x00\x00jobs [-lnprs] [jobspec .'
905639 ']\x00\x00\x00\x00jobs [-lnprs] [jobspec ...] or jobs -x '
905655 's] [jobspec ...] or jobs -x command [args]\x00\x00'
905699 '\x00disown [-h] [-ar] [jobspec ... | pid ...]\x00\x00'
905775 'm | -sigspec] pid | jobspec ... or kill -l ['
910414 't\x00There are stopped jobs.\n\x00There are running'
910439 '\n\x00There are running jobs.\n\x00exit\n\x00logout\n\x00not'
911874 'ns/../.././builtins/jobs.def\x00lpnxrs\x00jobs_bui'
911890 'ins/jobs.def\x00lpnxrs\x00jobs_builtin\x00ahr\x00Unknown'
914528 'pell\x00checkhash\x00checkjobs\x00checkwinsize\x00cmdhis'
$
```

## Notes

- Data must be fed through stdin.
