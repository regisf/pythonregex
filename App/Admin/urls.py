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
Define urls for the adminstration part
"""

__author__ = 'Regis FLORET'

from App.Admin.mainhandler import AdminHandler, LoginHandler, LogoutHandler
from App.Admin.usershandler import UsersHandler, UsersEditHandler, UsersDeleteHandler, UsersAddHandler
from App.Admin.emailshandler import EmailsHandler, EmailsAddHandler, EmailsDeleteHandler, EmailEditHandler
from App.Admin.preferencehandler import PreferenceHandler
from App.Admin.codeshandler import CodesHandler

URLS = [
    (r'^/admin/$', AdminHandler),
    (r'^/admin/login/$', LoginHandler),
    (r'^/admin/logout/$', LogoutHandler),

    (r'^/admin/users/$', UsersHandler),
    (r'^/admin/users/edit/(?P<name>\w+)/$', UsersEditHandler),
    (r'^/admin/users/add/$', UsersAddHandler),
    (r'^/admin/users/delete/(?P<name>\w+)/$', UsersDeleteHandler),

    (r'^/admin/emails/pref/$', PreferenceHandler),
    (r'^/admin/emails/$', EmailsHandler),
    (r'^/admin/emails/edit/(\w+)/$', EmailEditHandler),
    (r'^/admin/emails/add/$', EmailsAddHandler),
    (r'^/admin/emails/delete/(?P<name>.*?)/$', EmailsDeleteHandler),

    (r'/admin/codes/$', CodesHandler),
]


