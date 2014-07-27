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

import hashlib
import datetime

from . import database
from bson.objectid import ObjectId
import settings


class UserModel:
    """
    The UserModel is a wrapper to avoid direct database calls in the program
    """
    def __init__(self):
        """
        Ctor. Load the User collection
        """
        self.users = database.user

    def _generate_password(self, password):
        """
        Generate the hash password
        """
        return hashlib.sha256(settings.SECRET_KEY.encode() + password.encode()).hexdigest()

    def is_email_exists(self, email):
        """
        Test if an email exists
        """
        return self.users.find_one({'email': email}) is not None

    def create_user(self, username, email, password, temp=True, is_admin=False):
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

    def create_temp_user(self, username, email, password, hash):
        """
        Create an user not registred
        """
        return self.users.insert({
            'username': username,
            'email': email,
            'password': self._generate_password(password),
            'creation_date': datetime.datetime.now(),
            'is_admin': False,
            'temp_hash': hash
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

    def find_by_hash(self, hash):
        """
        Find an user by its temp_hash.
        """
        return self.users.find_one({'temp_hash': hash})

    def find_by_id(self, _id):
        return self.users.find_one({'_id': ObjectId(_id.decode('utf-8'))})

    def find_by_username(self, username):
        """
        Find an user by its username
        :param username:
        :return: A MongoDB object
        """
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
        return self.users.find_one({'username':name})

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