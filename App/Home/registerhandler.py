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
import time
import hashlib

import tornado.web
import tornado.gen

from App.models.user import UserModel
from App.models.email import EmailModel
from App.models.preference import PreferenceModel
from App.utils.email import send_mail
from App.utils.template import micro_template

import private_settings

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            'register.html',
            page='register',
            errors=False,
            username='',
            email='',
            fields=[],
            messages={},
            question=self.application.settings.get("question")
        )

    def post(self):
        username = self.get_argument('username')
        email = self.get_argument('email')
        password = self.get_argument('password')
        confirm = self.get_argument('confirm')
        question = self.get_argument('question')
        answer = self.get_argument('answer')

        error = []
        if question != answer:
            error.append({'message': "You didn't answer correctly to the question", "field": "question"})

        if not username:
            error.append({'message': 'The user name must be filled', 'field': 'username'})
        elif UserModel().is_username_exists(username):
            error.append({'message': 'The user name you choose already exists.', 'field': 'username'})

        if not email:
            error.append({'message': 'Email is required and must be valid', 'field': 'email'})
        elif UserModel().is_email_exists(email):
            error.append({'message': "Email exists, may be it's yours.", 'field': 'email'})

        if not password:
            error.append({'message': 'A password is required', 'field': 'password'})
        elif confirm != password:
            error.append({'message': 'The password and its confirmation are different', 'field': 'confirm'})

        if not error:
            mail_model = EmailModel()
            subject, body = mail_model.get_template('registration')
            registration_key = hashlib.md5(email.encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest()
            UserModel().create_temp_user(username, email, password, registration_key)
            keys = {
                'website': private_settings.SITE_NAME,
                'registration_key': registration_key
            }
            content = micro_template(body, keys)
            host_pref = PreferenceModel().get_mail_server()

            # FIXME: Should be async
            send_mail(host_pref['sender'], email, subject, content, host_pref)

            self.render(
                'register_success.html',
                page='register_success',
                email_receiver=email,
                question=self.application.settings.get("question")
            )
        else:
            messages = {}
            for err in error:
                messages[err['field']] = err['message']

            self.render(
                'register.html',
                page='register',
                errors=error,
                username=username,
                email=email,
                fields=[err['field'] for err in error],
                messages=messages,
                question=self.application.settings.get("question")
            )


class CheckEmailHandler(tornado.web.RequestHandler):
    def get(self):
        """
        Test if an email exists
        """
        email = self.get_argument('email')
        success = False
        exists = False
        if email is not None:
            #yield tornado.gen.Task()
            self.add_header('Content-Type', 'application/json')
            exists = UserModel().is_email_exists(email)

        self.write(json.dumps({'success': success, 'exists': exists, 'action': 'checkmail'}, ensure_ascii=False))


class ConfirmHandler(tornado.web.RequestHandler):
    def get(self, hash):
        """
        Confirm the inscription by mail
        """
        model = UserModel()
        user = model.find_by_hash(hash)
        if user:
            model.set_user_registered(user)
            self.render(
                "registration_confirm.html",
                error=False,
                question=self.application.settings.get('question')
            )
        else:
            self.render(
                "registration_confirm.html",
                error=True,
                question=self.application.settings.get("question")
            )


class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("OK")