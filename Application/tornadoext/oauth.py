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
#
# Exception: The following code is not a part of the project and belong the their respective owner

import urllib
import tornado.ioloop
import tornado.web
import tornado.auth
import tornado.httpclient
import tornado.escape
import tornado.httputil
import logging


class GithubMixin(tornado.auth.OAuth2Mixin):
    """
    GitHub OAuth connection.
    http://casbon.me/connecting-to-githubs-oauth2-api-with-tornado
    """

    _OAUTH_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    _OAUTH_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    _API_URL = 'https://api.github.com'

    def get_authenticated_user(self, redirect_uri, client_id, client_secret,
                               code, callback, extra_fields=None):
        """ Handles the login for Github, queries /user and returns a user object
        """
        logging.debug('gau ' + redirect_uri)
        http = tornado.httpclient.AsyncHTTPClient()
        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        http.fetch(
            self._oauth_request_token_url(**args),
            self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, extra_fields)
        )

    def _on_access_token(self, redirect_uri, client_id, client_secret,
                        callback, fields, response):
        """ callback for authentication url, if successful get the user details """
        if response.error:
            logging.warning('Github auth error: %s' % str(response))
            callback(None)
            return

        args = tornado.escape.parse_qs_bytes(
                tornado.escape.native_str(response.body))

        if 'error' in args:
            logging.error('oauth error ' + args['error'][-1])
            raise Exception(args['error'][-1])

        session = {
            "access_token": args["access_token"][-1],
        }

        self.github_request(
            method="/user",
            callback=self.async_callback(
                self._on_get_user_info, callback, session),
            access_token=session["access_token"],
            )

    def _on_get_user_info(self, callback, session, user):
        """ callback for github request /user to create a user """
        logging.debug('user data from github ' + str(user))
        if user is None:
            callback(None)
            return
        callback({
            "login": user["login"],
            "name": user["name"],
            "email": user["email"],
            "access_token": session["access_token"],
        })

    def github_request(self, path, callback, access_token=None,
                method='GET', body=None, **args):
        """ Makes a github API request, hands callback the parsed data """
        args["access_token"] = access_token
        url = tornado.httputil.url_concat(self._API_URL + path, args)
        logging.debug('request to ' + url)
        http = tornado.httpclient.AsyncHTTPClient()
        if body is not None:
            body = tornado.escape.json_encode(body)
            logging.debug('body is' +  body)
        http.fetch(url, callback=self.async_callback(
                self._parse_response, callback), method=method, body=body)

    def _parse_response(self, callback, response):
        """ Parse the JSON from the API """
        if response.error:
            logging.warning("HTTP error from Github: %s", response.error)
            callback(None)
            return
        try:
            json = tornado.escape.json_decode(response.body)
        except Exception:
            logging.warning("Invalid JSON from Github: %r", response.body)
            callback(None)
            return
        if isinstance(json, dict) and json.get("error_code"):
            logging.warning("Facebook error: %d: %r", json["error_code"],
                            json.get("error_msg"))
            callback(None)
            return
        callback(json)


class LinkedInMixin(tornado.auth.OAuth2Mixin):
    """
    LinkedIn authentication using OAuth2.
    By Youssouf Simonson : https://gist.github.com/ysimonson

    Example usage::

        class LinkedInLoginHandler(LoginHandler, LinkedInMixin):
            @tornado.gen.coroutine
            def get(self):
                code = self.get_argument("code", None)
                redirect_uri = "%s://%s%s" % (self.request.protocol, self.request.host, self.request.path)

                if not code:
                    # Generate a random state
                    state = binascii.b2a_hex(os.urandom(15))

                    self.set_secure_cookie("linkedin_state", state)

                    yield self.authorize_redirect(
                        redirect_uri=redirect_uri,
                        client_id=self.settings["linkedin_client_id"],
                        extra_params={
                            "response_type": "code",
                            "state": state,
                            "scope": "r_basicprofile r_emailaddress"
                        }
                    )

                    return

                # Validate the state
                if self.get_argument("state", None) != self.get_secure_cookie("linkedin_state"):
                    raise tornado.web.HTTPError(400, "Invalid state")

                user_data = yield self.get_authenticated_user(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["linkedin_client_id"],
                    client_secret=self.settings["linkedin_client_secret"],
                    code=code,
                    extra_fields=["formatted-name", "email-address"]
                )

                if not user_data:
                    raise tornado.web.HTTPError(400, "LinkedIn authentication failed")

                # Handle authenticated user
    """
    _OAUTH_ACCESS_TOKEN_URL = "https://www.linkedin.com/uas/oauth2/accessToken?"
    _OAUTH_AUTHORIZE_URL = "https://www.linkedin.com/uas/oauth2/authorization?"
    _OAUTH_NO_CALLBACKS = False

    @tornado.auth._auth_return_future
    def get_authenticated_user(self, redirect_uri, client_id, client_secret, code, callback, extra_fields=None):
        http = tornado.httpclient.AsyncHTTPClient()

        args = {
            "redirect_uri": redirect_uri,
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "extra_params": {
                "grant_type": "authorization_code"
            }
        }

        fields = set(['id'])

        if extra_fields:
            fields.update(extra_fields)

        http.fetch(self._oauth_request_token_url(**args), method="POST", body="",
            callback=self.async_callback(self._on_access_token, redirect_uri, client_id, client_secret, callback, fields))

    def _on_access_token(self, redirect_uri, client_id, client_secret, future, fields, response):
        if response.error:
            future.set_exception(tornado.auth.AuthError('LinkedIn auth error (%s): %s' % (response.code, response.body)))
            return

        args = tornado.escape.json_decode(response.body)
        expires_in = args["expires_in"]
        access_token = args["access_token"]

        self.linkedin_request(
            path="/v1/people/~:(%s)" % ",".join(fields),
            callback=self.async_callback(self._on_get_user_info, future, expires_in, access_token),
            access_token=access_token,
        )

    def _on_get_user_info(self, future, expires_in, access_token, user):
        if user is None:
            future.set_result(None)
            return

        user["access_token"] = access_token
        user["expires_in"] = expires_in
        future.set_result(user)

    @tornado.auth._auth_return_future
    def linkedin_request(self, path, callback, method="GET", access_token=None, post_args=None, query_args=None):
        url = "https://api.linkedin.com" + path

        # Build the query parameters
        all_query_args = dict(query_args or {})

        if access_token:
            all_query_args["oauth2_access_token"] = access_token

        if all_query_args:
            url += "?" + urllib.urlencode(all_query_args)

        # Build the request body. Empty bodies must be either set to an empty
        # string or None based on the request method. This is because the
        # Tornado HTTP client aggressively throws errors based on the request
        # method / body content combination.
        if self.request.method in ("POST", "PATCH", "PUT"):
            if post_args:
                body = urllib.urlencode(post_args)
            else:
                body = ""
        else:
            body = None

        wrapped_callback = self.async_callback(self._on_linkedin_request, callback)
        http = tornado.httpclient.AsyncHTTPClient()

        # Ask linkedin to send us JSON on all API calls (not xml)
        headers = tornado.httputil.HTTPHeaders({"x-li-format":"json"})

        http.fetch(url, method=method, headers=headers, body=body, callback=wrapped_callback)

    def _on_linkedin_request(self, future, response):
        if response.error:
            future.set_exception(tornado.auth.AuthError("LinkedIn error (%s) when requesting %s: %s" % (response.code, response.request.url, response.body)))
        else:
            future.set_result(tornado.escape.json_decode(response.body))
