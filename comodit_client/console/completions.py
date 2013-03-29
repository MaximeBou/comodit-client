# coding: utf-8

import readline, paths

from comodit_client.console.utils import merge_escaped

class Completer(object):
    def __init__(self, cmds, current):
        self._cmds = cmds
        self._current = current
        self._last_path = None
        self._last_item = None

    def _get_item_path(self, incomplete_path):
        last_slash = incomplete_path.rfind('/')
        if last_slash == 0:
            return '/'
        elif last_slash > 0:
            return incomplete_path[0:last_slash]
        else:
            return ''

    def _escape(self, txt):
        return txt.replace(' ', '\\ ')

    def __call__(self, text, state):
        line = readline.get_line_buffer().lstrip()
        return self.complete(line, text, state)

    def _next_item(self, item_path):
        return paths.change_with_elems(self._current._client, paths.absolute_elems(self._current, item_path), None)

    def _strip_options(self, tokens):
        cmd = tokens[0]
        stripped = [cmd]
        i = 1
        while i < len(tokens):
            t = tokens[i]
            if t.startswith('-'):
                if self._cmds.has_value(cmd, t):
                    i += 1  # skip also next token
            else:
                stripped.append(t)
            i += 1
        return stripped

    def complete(self, line, text, state):
        tokens = merge_escaped(line.split())
        complete_cmd = len(tokens) == 0 or (len(tokens) == 1 and not line.endswith(' '))

        values = []
        if complete_cmd:
            values = self._cmds.get_commands()
        elif (len(tokens) > 0) and text.startswith('-'):
            values = self._cmds.get_options(tokens[0])
        else:
            tokens = self._strip_options(tokens)
            item_path = self._get_item_path(tokens[1] if len(tokens) > 1 else '')
            if item_path != self._last_path:
                self._last_path = item_path
                self._last_item = self._next_item(item_path)

            for c in self._last_item.children_conts:
                values.append(c + "/")

            for c in self._last_item.children_leaves:
                values.append(c)

        options = [i for i in values if i.startswith(text)]
        options.sort()
        if state < len(options):
            return self._escape(options[state])
