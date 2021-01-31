let s:cache_directory_path = "~/.cache/denite-bookmark"
let s:cache_file_name = "bookmark.json"
let s:default_group_name = "default"
let s:default_kinds = "buffer,directory,file,openable"


function! denite#bookmark#init()
  call denite#bookmark#set_add_action(s:default_kinds)
endfunction

function! denite#bookmark#set_add_action(kind)
	call denite#custom#action(a:kind, "add_bookmark", function("s:add_action"))
endfunction

function! denite#bookmark#set_cache_directory_path(path)
  let s:cache_directory_path = a:path
endfunction

function! denite#bookmark#get_cache_directory_path()
  return fnamemodify(s:cache_directory_path, ":p")
endfunction

function! denite#bookmark#get_cache_file_path()
  return denite#bookmark#get_cache_directory_path() . "/" . s:cache_file_name
endfunction

function! denite#bookmark#set_default_group(group)
  let s:default_group_name = a:group
endfunction

function! denite#bookmark#get_default_group()
  return s:default_group_name
endfunction

function! s:add_action(context)
  python3 << EOF
import vim
from importlib import import_module

path_list = []
for path in vim.call(
        'globpath', vim.options['runtimepath'],
        'rplugin/python3/denite', 1).split('\n'):
    path_list.append(path)
    sys.path.append(path)

import bookmark.action as action
action.add_bookmark(vim, vim.eval('a:context'))

for path in path_list:
    sys.path.remove(path)
EOF
endfunction
