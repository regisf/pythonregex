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

import binascii
import json
import os

from tornado.auth import GoogleOAuth2Mixin, TwitterMixin, FacebookGraphMixin
from tornado.gen import coroutine
from tornado.web import authenticated, HTTPError

from App.models.preference import Config
from App.models.user import UserModel
from tornadoext.oauth import GithubMixin, LinkedInMixin
from tornadoext.requesthandler import RequestHandler


class LoginHandler(RequestHandler):
    """
    Connect the user
    """
    def post(self):
        model = UserModel()
        email = self.get_argument("email")
        password = self.get_argument("password")
        message = "Unknow user (bad email or wrong password). You should retry."
        message_level = 1

        if email and password:
            user = model.validate_user(email, password)
            if user:
                self.login(user)
                message = "You are now connected."
                message_level = 0

        self.add_flash_message(message_level, message)
        self.redirect('/')


class LogoutHandler(RequestHandler):
    """
    Disconnect the user and go to the main page
    """

    @authenticated
    def get(self):
        self.add_flash_message(0, "You are now disconnected.")
        self.logout()
        self.redirect('/')


class GoogleOAuth2Handler(RequestHandler, GoogleOAuth2Mixin):
    """
    Connect with Google account
    """

    @coroutine
    def get(self, *args, **kwargs):
        redirect_uri = "%s://%s" % (self.request.protocol, "python-regex.com/auth/google/")
        if self.get_argument('code', False):
            config = Config()
            if self._OAUTH_SETTINGS_KEY not in self.settings:
                self.settings[self._OAUTH_SETTINGS_KEY] = {
                    'key': config.get('google_consumer_key'),
                    'secret': config.get('google_secret_key')
                }
            user = yield self.get_authenticated_user(
                redirect_uri=redirect_uri,
                code=self.get_argument('code')
            )

            access_token = str(user['access_token'])
            http_client = self.get_auth_http_client()
            response = yield http_client.fetch('https://www.googleapis.com/oauth2/v1/userinfo?access_token={}'
                                               .format(access_token))

            if not response:
                HTTPError(500, "Google authentication error")
                return

            user_json = json.loads(response.body.decode())
            user = UserModel().create_social_user(
                user_json.get('name'),
                'google',
                user_json.get('email', ''),
                user_json.get('picture', '')
            )
            self.login(user)
            self.redirect('/')
            return

        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=Config().get('google_consumer_key'),
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class TwitterOAuth2Handler(RequestHandler, TwitterMixin):
    """
    Connect with Twitter account
    """

    @coroutine
    def get(self, *args, **kwargs):
        if self.get_argument("oauth_token", None):
            yield self.get_authenticated_user(
                callback=self._on_login
            )
        else:
            yield self.authorize_redirect()

    def _on_login(self, user):
        username = user['name']
        user = UserModel().create_social_user(username, 'twitter')
        self.login(user)
        self.redirect('/')


class FacebookOAuth2Handler(RequestHandler, FacebookGraphMixin):
    @coroutine
    def get(self):
        config = Config()
        client_id = config.get('facebook_api_key')
        client_secret = config.get('facebook_secret')

        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                redirect_uri='/auth/facebook/',
                client_id=client_id,
                client_secret=client_secret,
                code=self.get_argument("code")
            )
            # Save the user with e.g. set_secure_cookie

        else:
            yield self.authorize_redirect(
                redirect_uri='/auth/facebook/',
                client_id=client_secret,
                extra_params={"scope": "read_stream,offline_access"}
            )


class LinkedInOAuth2Handler(RequestHandler, LinkedInMixin):
    """
    Connect with LinkedIn API
    """

    @coroutine
    def get(self, *args, **kwargs):
        config = Config()
        code = self.get_argument("code", None)
        redirect_uri = "%s://%s" % (self.request.protocol, "python-regex.com/auth/linkedin/")

        if not code:
            # Generate a random state
            state = binascii.b2a_hex(os.urandom(15))

            self.set_secure_cookie("linkedin_state", state)

            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=config.get("linkedin_api_key"),
                extra_params={
                    "response_type": "code",
                    "state": state,
                    "scope": "r_basicprofile r_emailaddress"
                }
            )

            return

        # Validate the state
        if self.get_argument("state", None) != self.get_secure_cookie("linkedin_state"):
            raise HTTPError(400, "Invalid state")

        user_data = yield self.get_authenticated_user(
            redirect_uri=redirect_uri,
            client_id=config.get("linkedin_consumer_key"),
            client_secret=config("linkedin_consumer_secret"),
            code=code,
            extra_fields=["formatted-name", "email-address"]
        )

        if not user_data:
            raise HTTPError(400, "LinkedIn authentication failed")

        print(user_data)


class GithubOAuth2Handler(RequestHandler, GithubMixin):
    """
    Connect with GitHub API
    """

    @coroutine
    def get(self, *args, **kwargs):
        redirect_uri = '/auth/github/'
        config = Config()
        client_id = config.get('github_consumer_key')
        client_secret = config.get('github_consumer_secret')

        if self.get_argument("code", False):
            self.get_authenticated_user(
                redirect_uri=redirect_uri,
                client_id=client_id,
                client_secret=client_secret,
                code=self.get_argument("code"),
                callback=self._on_login
            )
            return

        self.authorize_redirect(
            redirect_uri=redirect_uri,
            client_id=client_id,
            extra_params={"scope": "user", "foo": 1}
        )

    def _on_login(self, user):
        print(user)
