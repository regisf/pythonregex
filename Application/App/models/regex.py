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

import datetime

from bson.dbref import DBRef
from bson.objectid import ObjectId

from . import database
from .user import UserModel


class RegexModel(object):
    def __init__(self):
        self.db = database.saved_regex

    def get_all_for_user(self, user):
        """
        Get all regex for an user
        :param user: A MongoDB object that describes the user
        :return: All the regex
        """
        return self.db.find({
            'user': DBRef(collection='user', id=user['_id'])
        })

    def save_for_user(self, name, regex, user):
        """
        Save a regular expression for the user

        :raise AttributeError on user error
        :type name: str
        :param name: The username
        :type regex: str
        :param regex: The regular expression
        :type user: dict
        :param user: The user as a dict
        :rtype: dict
        :return: The mongo object as dict
        """
        saved = self.find_by_name(name, user)
        user = UserModel().find_by_username(user.get('username'))

        if not user:
            raise AttributeError("Not yours")

        if not saved:
            return self.db.insert({
                'regex': regex,
                'name': name,
                'last_update': datetime.datetime.now(),
                'user': DBRef(collection="user", id=user['_id'])
            })
        else:
            return self.db.update(
                {'_id': saved.get('_id')},
                {'$set': {
                    'regex': regex,
                    'last_update': datetime.datetime.now()
                }}
            )

    def find_by_name(self, name, user):
        return self.db.find_one({'name': name, 'user': DBRef(collection='user', id=user['_id'])})

    def delete(self, user, _id):
        """
        Delete a Regex
        :param user: A MongoDB user entry
        :param _id:  The regex id_
        """
        self.db.remove({'_id': ObjectId(_id), 'user': DBRef(collection='user', id=user['_id'])})

    def count(self):
        """
        Count how many entries
        :return: The number of entries
        """
        return self.db.count()
