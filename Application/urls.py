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

"""
Contains all public urls for the WebSite
"""

import tornado.web

import settings

from App.Home.homehandler import HomeHandler
from App.Home.ajaxhandler import AjaxHandler
from App.Home.websockethandler import WebSocketHandler
from App.Home.registerhandler import RegisterHandler, ConfirmHandler
from App.Home.contacthandler import ContactHandler
from App.Home.connecthandler import (LoginHandler, LogoutHandler, GoogleOAuth2Handler, TwitterOAuth2Handler,
                                     FacebookOAuth2Handler, LinkedInOAuth2Handler, GithubOAuth2Handler)
from App.User.profile import AccountProfileHandler
from App.User.regex import AccountRegexHandler

from App.Admin.urls import URLS as AdminURLS

URLS = [
    (r'^/assets/(.*)', tornado.web.StaticFileHandler, {'path': settings.STATIC_FILES}),

    (r'^/$', HomeHandler),
    (r'^/contact$', ContactHandler),

    (r'^/auth/confirm/(?P<hash>\w+)', ConfirmHandler),
    (r'^/auth/register/$', RegisterHandler),
    (r'^/auth/login/$', LoginHandler),
    (r'^/auth/logout/$', LogoutHandler),

    (r'^/auth/google/$', GoogleOAuth2Handler),
    (r'^/auth/twitter/$', TwitterOAuth2Handler),
    (r'^/auth/facebook/$', FacebookOAuth2Handler),
    (r'^/auth/linkedin/$', LinkedInOAuth2Handler),
    (r'^/auth/github/$', GithubOAuth2Handler),

    (r'^/wsa/$', AjaxHandler),
    (r'^/ws/$', WebSocketHandler),

    (r'^/user/profile/$', AccountProfileHandler),
    (r'^/user/regex/$', AccountRegexHandler),
    (r'^/user/regex/delete/$', AccountRegexHandler)

] + AdminURLS

