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

from App.models.user import UserModel
from tornadoext.requesthandler import RequestHandler, admin_auth_required


class UsersHandler(RequestHandler):
    @admin_auth_required
    def get(self):
        """
        Display all users
        """
        self.render('admin/users/list.html', users=UserModel().all())


class UsersEditHandler(RequestHandler):
    @admin_auth_required
    def get(self, name):
        """
        Display the user information
        """
        self.render('admin/users/edit.html', user=UserModel().get_by_name(name))

    @admin_auth_required
    def post(self, name):
        """
        Save the user modification
        """
        add_another = 'add_another' in self.request.arguments
        continue_edit = 'continue_edit' in self.request.arguments
        email = self.get_argument('email')
        creation_date = self.get_argument('creation_date')
        is_admin = self.get_argument('is_admin') == 'on'

        user_model = UserModel()
        user_model.edit(name, creation_date, email, is_admin)
        if add_another:
            self.redirect('/admin/users/add/')
        elif continue_edit:
            self.render('admin/users/edit.html', user=user_model.get_by_name(name))
        else:
            self.redirect('/admin/users/')


class UsersDeleteHandler(RequestHandler):
    @admin_auth_required
    def get(self, name):
        """
        Confirm page
        """
        self.render('admin/users/delete.html', username=name)

    @admin_auth_required
    def post(self, name):
        """
        Execution page
        """
        # TODO: Test if the user to delete is not the user and not the last admin
        UserModel().delete(name)
        self.redirect('/admin/users/')


class UsersAddHandler(RequestHandler):
    """
    Add a new user
    """

    @admin_auth_required
    def get(self):
        self.render('admin/users/add.html', errors={})

    @admin_auth_required
    def post(self):
        """
        The user is created
        """
        errors = {}

        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        is_admin = self.get_argument('is_admin', 'off') == 'on'

        if not email:
            errors['email'] = 'An email address is required'

        if not username:
            errors['username'] = 'Username cannot be empty'

        if not password:
            errors['password'] = 'Password is empty'

        if errors.keys():
            self.render('admin/users/add.html', errors=errors)

        UserModel().create_user(username, email, password, is_admin=is_admin)
        self.redirect('/admin/users/')
