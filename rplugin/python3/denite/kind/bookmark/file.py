import os
import json
from denite.kind.file import Kind as File

class Kind(File):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'bookmark/file'
        self.default_action = 'open'

    def action_delete(self, context):
        self._delete_bookmark(context['targets'][0])

    def _delete_bookmark(self, target):
        group = target['action__group']
        name = target['action__name']

        try:
            bookmark_dict = _read(self.vim)
        except FileNotFoundError:
            return

        group_dict = bookmark_dict.get(group)

        if not group_dict:
            return

        group_dict['bookmarks'] = [
                d for d in group_dict['bookmarks'] if d['name'] != name
                ]

        _write(self.vim, bookmark_dict)

def _read(vim):
    with open(vim.call('bookmark#get_cache_file_path')) as f:
        return json.loads(f.read())

def _write(vim, bookmark_dict):
    dir_path = vim.call('bookmark#get_cache_directory_path')
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    with open(vim.call('bookmark#get_cache_file_path'), 'w') as f:
        json.dump(bookmark_dict, f, ensure_ascii=False, indent=2)

