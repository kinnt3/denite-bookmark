import os
import sys
import json
from denite.source.file import Source as File

bookmark_HIGHLIGHT_SYNTAX = [
    {'name': 'Denite_bookmark_Name', 'link': 'Statement', 're': r'\[.*\]\ze\s'}
]

class Source(File):
    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'bookmark'

    def highlight(self):
        for syn in bookmark_HIGHLIGHT_SYNTAX:
            self.vim.command(
                'syntax match {0}_{1} /{2}/ contained containedin={0}'.format(
                    self.syntax_name, syn['name'], syn['re']
                )
            )
            self.vim.command(
                'highlight default link {0}_{1} {2}'.format(
                    self.syntax_name, syn['name'], syn['link']
                )
            )

    def gather_candidates(self, context):
        group = (
            context['args'][0]
            if len(context['args']) >= 1
            else self.vim.call('denite#bookmark#get_default_group')
        )

        if not group or group == '':
            raise ValueError('group value is invalid:{}'.format(group))

        try:
            bookmark_dict = _read(self.vim)
        except FileNotFoundError:
            return []

        group_dict = bookmark_dict.get(group, None)

        if not group_dict:
            return []

        return [
            {
                'word': f"[{v['name']}] {v['path']}",
                'action__name': v['name'],
                'action__group': group,
                'action__path': v['path'],
                'kind': 'bookmark/directory' if os.path.isdir(v['path']) else 'bookmark/file'
            }
            for v in group_dict['bookmarks']
        ]

def _read(vim):
    with open(vim.call('denite#bookmark#get_cache_file_path')) as f:
        return json.loads(f.read())
