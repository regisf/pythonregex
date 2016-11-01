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
import hashlib

from bson.objectid import ObjectId

from . import database
from .preference import Config


class UserModel:
    """
    The UserModel is a wrapper to avoid direct database calls in the program
    """

    def __init__(self):
        """
        Ctor. Load the User collection
        """
        self.users = database.user

    @classmethod
    def _generate_password(cls, password):
        """
        Generate the hash password
        """
        config = Config()
        return hashlib.sha256(config.get('secret_key').encode() + password.encode()).hexdigest()

    def is_email_exists(self, email):
        """
        Test if an email exists

        :param email: The email to test
        :type email: str
        :return: True if the user is found False elsewhere
        :rtype: bool
        """
        return self.users.find_one({'email': email}) is not None

    def create_user(self, username, email, password, is_admin=False):
        """
        Create an user
        If temp is set to True, an hash is generated
        """
        return self.users.insert({
            'username': username,
            'email': email,
            'password': self._generate_password(password),
            'creation_date': datetime.datetime.now(),
            'is_admin': is_admin
        })

    def create_social_user(self, username, network, email='', avatar=''):
        """
        Create a user coming from a social network
        :param username: The given username
        :rtype username: str
        :param network: Which network does he/she comes from
        :rtype network: str
        :param email: The user email
        :rtype email: str
        :param avatar: The url of the user avatar
        :rtype avatar: str
        :return: The user entry
        """
        user = self.find_by_username(username)
        if not user:
            user_id = self.users.insert({
                'username': username,
                'email': email,
                'from': network,
                'creation_date': datetime.datetime.now(),
                'is_admin': False,
                'temp_hash': None,
                'avatar': avatar
            })
            user = self.find_by_id(user_id)

        return user

    def create_temp_user(self, username, email, password, hashcode):
        """
        Create an user not registered
        """
        return self.users.insert({
            'username': username,
            'email': email,
            'password': self._generate_password(password),
            'creation_date': datetime.datetime.now(),
            'is_admin': False,
            'temp_hash': hashcode
        })

    def edit(self, username, creation_date, email, is_admin):
        """
        Modify entry
        """
        self.users.update(
            {'username': username},
            {'$set': {
                'username': username,
                'creation_date': datetime.datetime.strptime(creation_date, "%Y-%m-%d %H:%M:%S.%f"),
                'is_admin': is_admin,
                'email': email
            }}
        )

    def find_by_hash(self, hashcode):
        """
        Find an user by its temp_hash.
        """
        return self.users.find_one({'temp_hash': hashcode})

    def find_by_id(self, _id):
        return self.users.find_one({'_id': ObjectId(_id.decode('utf-8'))})

    def find_by_username(self, username):
        """
        Find an user by its username
        :param username:
        :return: A MongoDB object
        """
        if isinstance(username, str):
            return self.users.find_one({'username': username})

        return self.users.find_one({'username': username.decode('utf-8')})

    def set_user_registered(self, user):
        """
        Set the user as an active user
        """
        self.users.update({'_id': user['_id']}, {'$set': {'temp_hash': None}})

    def is_username_exists(self, username):
        """
        Find an user admin matching the username and his the password
        """
        return self.users.find_one({
            'username': username
        })

    def all(self, ):
        """
        Get all users at once
        """
        return self.users.find()

    def get_last_ten(self):
        """ Get last 10 users for the admin front page
        """
        return self.users.find()[:9]

    def get_by_name(self, name):
        """ Get a user by its username
        """
        return self.users.find_one({'username': name})

    def delete(self, name):
        """
        Delete the entry
        """
        self.users.remove({'username': name})

    def validate_user(self, email, password):
        """
        Find an user by its email and password
        """
        return self.users.find_one({'email': email, 'password': self._generate_password(password)})

    def exists(self, username, password, is_admin=False):
        """
        Test if there's an entry
        :param username:  The User name
        :param password:  the user password
        :param is_admin:  is the user an admin
        :return: The user entry or None
        """
        return self.users.find_one({
            'username': username,
            'password': self._generate_password(password),
            'is_admin': is_admin
        })
