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

"""
Email model
"""

from . import database


class EmailModel:
    def __init__(self):
        self.email = database.email
        self.pref = database.email_pref

    def get_template(self, shortcut):
        """
        Get a template from it's shortcut
        """
        template = self.email.find_one({'shortcut': shortcut})
        if template:
            return template['title'], template['content']

        return None, None

    def shortcut_exists(self, name):
        """
        Test if a shortcut exists
        """
        return self.email.find_one({'shortcut': name}) is not None

    def find_by_shortcut(self, short):
        """ Find an email with its shortcut """
        return self.email.find_one({'shortcut': short})

    def all(self, ):
        """ Get all emails in database """
        return self.email.find()

    def delete(self, shortcut):
        """ Delete a particular email. The key is the shortcut """
        self.email.remove({'shortcut': shortcut})

    def add_email(self, title, shortcut, content):
        """ Add an email """
        self.email.insert({
            'title': title,
            'shortcut': shortcut,
            'content': content
        })

    def edit_email(self, previous_shortcut, title, shortcut, content):
        """ Update an entry """
        self.email.update(
            {'shortcut': previous_shortcut},
            {'$set': {'title': title, 'shortcut': shortcut, 'content': content}}
        )


