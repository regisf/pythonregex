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

from tornadoext.requesthandler import RequestHandler, admin_auth_required

from App.models.preference import Config


class CodesHandler(RequestHandler):
    """
    Handle all codes for analytics or twitter,
    """
    @admin_auth_required
    def get(self):
        config = Config()
        self.render(
            "admin/codes/list.html",
            facebook=config.get('facebook', ''),
            twitter_consumer_key=config.get('twitter_consumer_key', ''),
            twitter_consumer_secret=config.get('twitter_consumer_secret', ''),
            google=config.get('google_client_id', ''),
            linkedin=config.get('linkedin', ''),
            github=config.get('github', ''),
            analytics=config.get('google_analytics_id', '')
        )

    @admin_auth_required
    def post(self):
        """
        Save the codes
        """
        config = Config()
        config.set('google_analytics_id', self.get_argument('analytics'))
        config.set('twitter_consumer_key', self.get_argument('twitter_consumer_key'))
        config.set('twitter_consumer_secret', self.get_argument('twitter_consumer_secret'))

        # PreferenceModel().save_codes(
        #     analytics=self.get_argument('analytics'),
        #     facebook_id=self.get_argument('facebook_app_id'),
        #     facebook_key=self.get_argument('facebook_secret_key'),
        #     google_id=self.get_argument('google_app_id'),
        #     google_key=self.get_argument('google_secret_key'),
        #     twitter_id=self.get_argument('twitter_app_id'),
        #     twitter_key=self.get_argument('twitter_secret_key'),
        #     linkedin_id=self.get_argument('linkedin_app_id'),
        #     linkedin_key=self.get_argument('linkedin_secret_key'),
        #     github_id=self.get_argument('github_app_id'),
        #     github_key=self.get_argument('github_secret_key'),
        # )

        self.redirect('/admin/codes/')