" This is a .exrc that I like to use to disable coloring in vi/vim based on syntax and content:

" syntax off
" let g:loaded_matchparen=1

set nocp
set noincsearch
set nohlsearch
set noshowmatch

" From https://stackoverflow.com/questions/237289/vim-configure-line-number-coloring
" even with these settings, if you turn on line numbering, the numbers could be rendered in a dopey color that can't be read well against the background.  I was using a white background and the default color for line numbers was a bright yellow which didn't show up well.  Initially, my thought was to make this `black` but then it didn't show up if the background was black.  `grey` is a good compromise.
highlight LineNr ctermfg=grey

