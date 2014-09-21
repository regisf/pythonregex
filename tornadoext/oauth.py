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


class LinkedInMixin(tornado.auth.OAuthMixin):
    """
    LinkedIn OAuth connection.
    https://gist.github.com/bootandy/4555500
    """

    _OAUTH_REQUEST_TOKEN_URL = "https://api.linkedin.com/uas/oauth/requestToken"
    _OAUTH_ACCESS_TOKEN_URL = "https://api.linkedin.com/uas/oauth/accessToken"
    _OAUTH_AUTHORIZE_URL = "https://www.linkedin.com/uas/oauth/authorize"
    _OAUTH_AUTHENTICATE_URL = "https://www.linkedin.com/uas/oauth/authenticate"
    _OAUTH_VERSION = "1.0"
    _OAUTH_NO_CALLBACKS = False
    #  http://developer.linkedin.com/docs/DOC-1002
    _DEFAULT_USER_FIELDS = "(id,first-name,last-name,headline,industry,positions,educations,summary,picture-url)"

    def authenticate_redirect(self):
        """Just like authorize_redirect(), but auto-redirects if authorized.

        This is generally the right interface to use if you are using
        LinkedIn for single-sign on.
        """
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch(self._oauth_request_token_url(), self.async_callback(
            self._on_request_token, self._OAUTH_AUTHENTICATE_URL, None))

    def linkedin_request(self, path, callback, access_token=None, post_args=None, **args):
        url = "http://api.linkedin.com" + path
        if access_token:
            all_args = {}
            all_args.update(args)
            all_args.update(post_args or {})
            method = "POST" if post_args is not None else "GET"
            oauth = self._oauth_request_parameters(
                url, access_token, all_args, method=method)
            args.update(oauth)
        if args:
            url += "?" + urllib.urlencode(args)
        callback = self.async_callback(self._on_linkedin_request, callback)
        http = tornado.httpclient.AsyncHTTPClient()
        # ask linkedin to send us JSON on all API calls (not xml)
        headers = tornado.httputil.HTTPHeaders({"x-li-format": "json"})
        if post_args is not None:
            http.fetch(url, method="POST", headers=headers, body=urllib.urlencode(post_args), callback=callback)
        else:
            http.fetch(url, headers=headers, callback=callback)

    def _parse_user_response(self, callback, user):
        callback(user)

    def _on_linkedin_request(self, callback, response):
        if response.error:
            logging.warning("Error response %s fetching %s", response.error, response.request.url)
            callback(None)
        else:
            callback(tornado.escape.json_decode(response.body))

    def _oauth_consumer_token(self):
        self.require_setting("linkedin_consumer_key", "LinkedIn OAuth")
        self.require_setting("linkedin_consumer_secret", "LinkedIn OAuth")
        return dict(
            key=self.settings["linkedin_consumer_key"],
            secret=self.settings["linkedin_consumer_secret"])

    def _oauth_get_user(self, access_token, callback):
        callback = self.async_callback(self._parse_user_response, callback)
        self.linkedin_request("/v1/people/~:%s" % self._DEFAULT_USER_FIELDS, access_token=access_token, callback=callback)

