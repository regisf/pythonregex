
__author__ = 'Régis FLORET'

import hashlib
import time

from tornadoext.requesthandler import RequestHandler

from App.models.user import UserModel
from App.models.email import EmailModel
from App.models.preference import PreferenceModel

from App.utils.email import is_email
from App.utils.email import send_mail
from App.utils.template import micro_template

import private_settings

class AccountProfileHandler(RequestHandler):
    def get(self, *args, **kwargs):
        """
        Display the information page
        """
        self.render("profile.html")

    def post(self, *args, **kwargs):
        """
        Change the information. If the usermail change, an email will be sended
        """
        if self.get_secure_cookie('connected'):
            username = self.get_argument('name')
            email = self.get_argument("email")
            password = self.get_argument("password")
            confirm = self.get_argument('confirm')
            current = UserModel().find_by_id(self.get_secure_cookie('connected'))

            error = []

            if not username:
                error.append({'message': 'The user name must be filled', 'field': 'username'})
            elif current['username'] != username and UserModel().is_username_exists(username):
                error.append({'message': 'The user name you choose already exists.', 'field': 'username'})

            if not email:
                error.append({'message': 'Email is required and must be valid', 'field': 'email'})
            elif current['email'] != email and is_email(email) and UserModel().is_email_exists(email):
                error.append({'message': "Email exists, may be it's yours.", 'field': 'email'})

            if password and confirm != password:
                error.append({'message': 'The password and its confirmation are different', 'field': 'confirm'})

            if not error:
                mail_model = EmailModel()
                subject, body = mail_model.get_template('changing_mail_confirmation')
                registration_key = hashlib.md5(email.encode('utf-8') + str(time.time()).encode('utf-8')).hexdigest()
                #UserModel().create_temp_user(username, email, password, registration_key)
                keys = {
                    'website': private_settings.SITE_NAME,
                    'registration_key': registration_key
                }
                content = micro_template(body, keys)
                host_pref = PreferenceModel().get_mail_server()

                send_mail(host_pref['sender'], email, subject, content, host_pref)

                self.render(
                    'profile.html',
                    errors=None,
                    fields=None,
                    error_message=None,
                    messages=[{'level': 0, 'message': 'Your account has been successfully updated'}]
                )
            else:
                print(error)
                errors = {}
                for err in error:
                    errors[err['field']] = err['message']

                self.render(
                    'profile.html',
                    errors=error,
                    fields=[err['field'] for err in error],
                    error_messages=errors
                )
        else:
            self.redirect('/')