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
from tornado.web import RequestHandler, authenticated

from App.models.preference import PreferenceModel


class CodesHandler(RequestHandler):
    """
    Handle all codes for analytics or captcha, twitter,
    """
    @authenticated
    def get(self):
        pref = PreferenceModel().get_codes()
        if not pref:
            pref = {
                'analytics': {
                    'key': ''
                },
                'facebook': {
                    'app_id': '',
                    'secret_key': ''
                },
                'twitter': {
                    'app_id': '',
                    'secret_key': ''
                },
                'google': {
                    'app_id': '',
                    'secret_key': ''
                },
                'linkedin': {
                    'app_id': '',
                    'secret_key': ''
                },
                'github': {
                    'app_id': '',
                    'secret_key': ''
                }
            }
        if not 'recaptcha' in pref:
            pref['recaptcha'] = {}

        self.render(
            "admin/codes/list.html",
            facebook=pref['facebook'],
            twitter=pref['twitter'],
            google=pref['google'],
            linkedin=pref['linkedin'],
            github=pref['github'],
            analytics=pref['analytics'],
            recaptcha=pref['recaptcha']
        )

    @authenticated
    def post(self):
        """
        Save the codes
        """
        PreferenceModel().save_codes(
            analytics=self.get_argument('analytics'),
            recaptcha_private=self.get_argument('recaptcha_private'),
            recaptcha_public=self.get_argument('recaptcha_public'),
            facebook_id=self.get_argument('facebook_app_id'),
            facebook_key=self.get_argument('facebook_secret_key'),
            google_id=self.get_argument('google_app_id'),
            google_key=self.get_argument('google_secret_key'),
            twitter_id=self.get_argument('twitter_app_id'),
            twitter_key=self.get_argument('twitter_secret_key'),
            linkedin_id=self.get_argument('linkedin_app_id'),
            linkedin_key=self.get_argument('linkedin_secret_key'),
            github_id=self.get_argument('github_app_id'),
            github_key=self.get_argument('github_secret_key'),
        )

        self.redirect('/admin/codes/')