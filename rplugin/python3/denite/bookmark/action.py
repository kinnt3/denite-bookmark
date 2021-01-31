import os
import json

def add_bookmark(vim, context):
    _add_bookmark(vim, context['targets'][0])
    vim.command('redraw')
    vim.call('denite#util#echo',
             '',
             'Add bookmark!')

def _add_bookmark(vim, target):
    default_group_name = vim.call('denite#bookmark#get_default_group')
    group = str(vim.call('denite#util#input',
                         'Group name [' + default_group_name + ']: ',
                         '',
                         ''))
    name = str(vim.call('denite#util#input',
                        'Bookmark name: ',
                        '',
                        ''))

    if not group or group == '': group = default_group_name

    path = target['action__path']

    try:
        bookmark_dict = _read(vim)
    except FileNotFoundError:
        bookmark_dict = {}

    group_dict = bookmark_dict.setdefault(group, {
        "bookmarks": [],
    })

    group_dict['bookmarks'].append({
        'name': name,
        'path': path,
    })

    _write(vim, bookmark_dict)

def _read(vim):
    with open(vim.call('denite#bookmark#get_cache_file_path')) as f:
        return json.loads(f.read())

def _write(vim, bookmark_dict):
    dir_path = vim.call('denite#bookmark#get_cache_directory_path')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    with open(vim.call('denite#bookmark#get_cache_file_path'), 'w') as f:
        json.dump(bookmark_dict, f, ensure_ascii=False, indent=2)
