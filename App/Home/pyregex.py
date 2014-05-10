# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
# (c) Régis FLORET 2013 and later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import json
import re
import html

class PyRegex(object):
    def doTheJob(self, value):
        regex = value['regex']
        content = value['content']
        method = value['method']
        flags = self._prepare_flags(value['flags'])
        options = value['options']
        count = value.get('count', 0)

        try:
            count = int(count)
        except:
            count = 0

        if regex != '' or content != '':
            result = {}
            if method == 'search':
                result = self._do_search(regex,content, flags, options)
            elif method == 'match':
                result = self._do_match(regex, content, flags, options)
            elif method == 'findall':
                result = self._do_findall(regex, content, flags, options)
            elif method == 'sub':
                result = self._do_sub(regex, value['sub'], content, flags, options)
            elif method == 'subn':
                result = self._do_subn(regex, value['sub'], content, count, flags, options)
            elif method == 'split':
                result = self._do_split(regex, content, count, flags, options)

            if 'content' in result:
                # in case of no error
                result['content'] = html.escape(result['content'])

            return json.dumps(result, ensure_ascii=False)

        else:
            return json.dumps({'success': False})


    def _prepare_flags(self, flagsList):
        flags = 0
        str_flags = []
        for flag in flagsList:
            if flag == 'ignore':
                flags |= re.IGNORECASE
                str_flags.append('re.IGNORECASE')
            elif flag == 'debug':
                flags | re.DEBUG
                str_flags.append('re.DEBUG')
            elif flag == 'multiline':
                flags |= re.MULTILINE
                str_flags.append('re.MULTILINE')
            elif flag == 'dotall':
                flags |= re.DOTALL
                str_flags.append('re.DOTALL')
            elif flag == 'unicode':
                flags |= re.UNICODE
                str_flags.append('re.UNICODE')
            elif flag == 'verbose':
                flags |= re.VERBOSE
                str_flags.append('re.VERBOSE')
        return flags, '|'.join(str_flags)

    def _display_command(self, command, result, regex, content, flags):
        """
        Display the command line
        """
        return """>>> result = re.{command}(r'''{regex}''', '''{content}''', {flags})\n>>> result\n""".format(
                command=command,
                regex=regex,
                content=content,
                flags=flags[1],
            )

    def _display_groups(self, result):
        """
        Display the group as a string
        """
        r = ''
        if result is not None:
            group = ["result.group({0}) = {1}".format(i, result.group(i)) for i in range(0, len(result.groups()) +1 )]

            r = """\n>>> result.groups()\n{groups}\n{group}""".format(
                groups=result.groups() if result.groups() else '()',
                group='\n>>> '.join(group)
            )
        return r

    def _do_search(self,regex, content,  flags, options ):
        """ Do a re.search """
        try:
            result = re.search(regex, content, flags[0])
        except re.error as e:
            return {'success':False, 'error': str(e)}

        r = ''
        if 'displaycommand' in options:
            r = self._display_command('search', result, regex, content, flags)

        r += "{result}".format(result=result)
        r += self._display_groups(result)

        return {'success': True, 'content': r}

    def _do_match(self, regex, content, flags, options):
        """ do a re.match """
        try:
            result = re.match(regex, content, flags[0])
        except re.error as e:
            return { 'success':False, 'error': str(e) }

        r = ''
        if 'displaycommand' in options:
            r += self._display_command('match', result, regex, content, flags)
        r += "{result}".format(result=result)
        r += self._display_groups(result)
        return {'success': True, 'content': r }

    def _do_findall(self, regex, content, flags, options):
        """ Do a re.findall """
        try:
            result = re.findall(regex, content, flags[0])
        except re.error as e:
            return {'success':False, 'error': str(e)}

        r = ''
        if 'displaycommand' in options:
            r = """>>> result = re.findall(r'''{regex}''', '''{content}''', {flags})\n>>> result\n""".format(
                content=content,
                flags=flags[1],
                regex=regex
            )
        r += """{result}\n""".format(result=result)
        return {'success': True, 'content': r }

    def _do_sub(self, regex, replace, content, flags,options):
        """ Do a re.findall """
        if not replace:
            replace = ''

        try:
            result = re.sub(regex, replace, content, flags[0])
        except re.error as e:
            return { 'success':False, 'error': str(e) }

        r = ''
        if 'displaycommand' in options:
            r = """>>> result = re.sub(r'''{regex}''', '''{replace}''', '''{content}''', {flags})\n>>> result\n""".format(
                content=content,
                flags=flags[1],
                regex=regex,
                replace=replace
            )
        r += """{result}\n""".format(result=result)

        return {'success': True, 'content': r }


    def _do_subn(self, regex, replace, content, count, flags, options):
        """ Do a re.findall """
        if not replace:
            replace = ''

        try:
            result = re.subn(regex, replace, content, count, flags[0])
        except re.error as e:
            return { 'success':False, 'error': str(e) }

        r = ''
        if 'displaycommand' in options:
            r = """>>> result = re.subn(r'''{regex}''', '''{replace}''', '''{content}''', {count}, {flags})\n>>> result\n""".format(
                content=content,
                flags=flags[1],
                regex=regex,
                replace=replace,
                count=count
            )
        r += """{result}\n""".format(result=result)
        return {'success': True, 'content': r }

    def _do_split(self, regex, content, count, flags, options):
        """ Do a re.findall """
        try:
            result = re.split(regex, string=content, maxsplit=count, flags=flags[0])
        except re.error as e:
            return { 'success':False, 'error': str(e) }

        r = ''
        if 'displaycommand' in options:
            r = """>>> result = re.split(r'''{regex}''', '''{content}''', {count}, {flags})\n>>> result\n""".format(
                content=content,
                flags=flags[1],
                regex=regex,
                count=count
            )
        r += """{result}\n""".format(result=result)
        return {'success': True, 'content': r }
