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

from tornado.web import RequestHandler
from App.models.email import EmailModel
from App.models.preference import PreferenceModel


def control_arguments(handler, edit=False):
    """
    Get all arguments and control errors
    @type handler tornado.web.RequestHandler
    @return a Tuple
    """
    title = handler.get_argument('title')
    content = handler.get_argument('content')
    shortcut = handler.get_argument('shortcut')
    errors = {}

    if not title:
        errors['title'] = 'Title is required'

    if not content:
        errors['content'] = 'Content is required'

    if not shortcut:
        errors['shortcut'] = 'The shortcut is required'
    else:
        if not edit and EmailModel().shortcut_exists(shortcut):
            errors['shortcut'] = 'The shortcut exists yet'

    return errors, title, content, shortcut


class EmailsHandler(RequestHandler):
    def get(self):
        """
        Get all emails tempaltes
        """
        emails = EmailModel().all()
        pref = PreferenceModel().get_mail_server()
        self.render("admin/emails/emails.html", emails=emails, pref={
            'sender': '',
            'server_name': 'localhost',
            'server_port': '',
            'server_username': '',
            'server_password': '',
        })

    def post(self):
        """
        Save preferences
        """
        default_email = self.get_argument('defaultemail', '')
        server_name = self.get_argument('defaultemail', settings.DEFAULT_EMAIL)

class EmailsAddHandler(RequestHandler):
    def get(self):
        self.render("admin/emails/add.html", errors={}, title='', content='', shortcut='')

    def post(self, ):
        errors, title, content, shortcut = control_arguments(self)

        if not errors.keys():
            EmailModel().add_email(title, shortcut, content)
            self.redirect('/admin/emails/')
            return

        self.render('admin/emails/add.html', errors=errors,
                                             title=title,
                                             content=content,
                                             shortcut=shortcut)


class EmailEditHandler(RequestHandler):
    def get(self, shortcut):
        """ Display edit form """
        email = EmailModel().find_by_shortcut(shortcut)
        if not email:
            return

        self.render('admin/emails/edit.html', errors={}, email=email)

    def post(self, shortcut):
        """
        Handle save
        """
        errors, title, content, shortcut = control_arguments(self, True)

        if not errors.keys():
            EmailModel().edit_email(shortcut, title, shortcut, content)
            self.redirect('/admin/emails/')
            return

        email = dict(zip(['title', 'content', 'shortcut'], [title, content, shortcut]))
        self.render('admin/emails/edit.html', errors=errors, email=email)


class EmailsDeleteHandler(RequestHandler):
    def get(self, name):
        EmailModel().delete(name)
        self.redirect('/admin/emails/')
