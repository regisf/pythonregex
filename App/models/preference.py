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

from . import database


class Config:
    """
    Class to handler server preferences
    """
    def __init__(self):
        self.__db = database.configuration

    def get(self, key, default_value=None):
        item = self.__db.find_one({'key': key})
        return item['value'] if item else default_value

    def set(self, key, value):
        item = self.get(key)
        if item is None:
            self.__db.insert({'key': key, 'value': value})
        else:
            self.__db.update({'key': key}, {'$set': {'value': value}})


class PreferenceModel(object):
    @classmethod
    def save_mail_server(self, sender, server_name, server_port, username, password):
        """
        Save the default preferences
        """
        preferences = {
            'sender': sender,
            'name': server_name,
            'port': server_port,
            'username': username,
            'password': password
        }

        Config().set('smtp_server', preferences)

    @classmethod
    def get_mail_server(self):
        """ Get the default preferences
        """
        pref = Config().get('smtp_server', {
            'sender': '',
            'name': 'localhost',
            'port': '',
            'username': '',
            'password': ''
        })
        return pref

    @classmethod
    def get_codes(self):
        """
        Get the codes for registering
        """
        return Config().get('codes', {
            'analytics': {'key': ''},
            'facebook': {'app_id': '','secret_key': ''},
            'twitter': {'app_id': '','secret_key': ''},
            'google': {'app_id': '', 'secret_key': ''},
            'linkedin': {'app_id': '','secret_key': ''},
            'github': {'app_id': '','secret_key': ''}
        })

    def save_codes(self, **kwargs):
        """
        Save the codes
        """
        pref = self.get_codes()
        create = False

        if not pref:
            create = True
            pref = {
                'analytics': {
                    'key': ''
                },
                'facebook': {
                    'app_id': '',
                    'secret_key': ''
                },
                'twitter': {
                    'app_id': '',
                    'secret_key': ''
                },
                'google': {
                    'app_id': '',
                    'secret_key': ''
                },
                'linkedin': {
                    'app_id': '',
                    'secret_key': ''
                },
                'github': {
                    'app_id': '',
                    'secret_key': ''
                },

                'recaptcha': {
                    'private_key': '',
                    'public_key': ''
                }
            }

        if 'analytics' in kwargs:
            pref['analytics']['key'] = kwargs['analytics']

        if 'facebook_id' in kwargs:
            pref['facebook']['app_id'] = kwargs['facebook_id']

        if 'facebook_key' in kwargs:
            pref['facebook']['secret_key'] = kwargs['facebook_key']

        if 'twitter_id' in kwargs:
            pref['twitter']['app_id'] = kwargs['twitter_id']

        if 'twitter_key' in kwargs:
            pref['twitter']['secret_key'] = kwargs['twitter_key']

        if 'google_id' in kwargs:
            pref['google']['app_id'] = kwargs['google_id']

        if 'google_key' in kwargs:
            pref['google']['secret_key'] = kwargs['google_key']

        if 'linkedin_id' in kwargs:
            pref['linkedin']['app_id'] = kwargs['linkedin_id']

        if 'linkedin_key' in kwargs:
            pref['linkedin']['secret_key'] = kwargs['linkedin_key']

        if 'github_id' in kwargs:
            pref['github']['app_id'] = kwargs['github_id']

        if 'github_key' in kwargs:
            pref['github']['secret_key'] = kwargs['github_key']

        values = {'name': 'codes'}
        if create:
            values.update(pref)
            self.db.insert(values)
        else:
            self.db.update(values, pref)

