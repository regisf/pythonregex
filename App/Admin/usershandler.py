# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

from tornado.web import RequestHandler

from App.models.user import UserModel


class UsersHandler(RequestHandler):
    def get(self):
        """
        Display all users
        """
        self.render('admin/users/list.html', users=UserModel().all())


class UsersEditHandler(RequestHandler):
    def get(self, name):
        """
        Display the user information
        """
        self.render('admin/users/edit.html', user=UserModel().get_by_name(name))

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
    def get(self, name):
        """
        Confirm page
        """
        self.render('admin/users/delete.html', username=name)

    def post(self, name):
        """
        Execution page
        """
        #TODO: Test if the user to delete is not the user and not the last admin
        UserModel().delete(name)
        self.redirect('/admin/users/')


class UsersAddHandler(RequestHandler):
    """
    Add a new user
    """
    def get(self):
        self.render('admin/users/add.html', errors={})

    def post(self):
        """
        The user is created
        """
        errors = {}
        user_model = UserModel()

        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        confirm = self.get_argument('confirm')
        is_admin = self.get_argument('is_admin', 'off') == 'on'

        if not email:
            errors['email'] = 'An email address is required'

        if not username:
            errors['username'] = 'Username cannot be empty'
        # elif user_model.exists(username):
        #     errors['username'] = 'User name exists'

        if not password:
            errors['password'] = 'Password is empty'

        # if password and (password != confirm):
        #     errors['password'] = 'Password and its confirmation are different'

        add_another = 'add_another' in self.request.arguments
        continue_edit = 'continue_edit' in self.request.arguments

        if errors.keys():
            self.render('admin/users/add.html', errors=errors)

        UserModel().create_user(username, email, password, is_admin=is_admin)
        self.redirect('/admin/users/')