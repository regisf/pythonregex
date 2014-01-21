# -*- coding: utf-8 -*-
#
# Python-regex.com : Regular expression as in Kodos3 but for the web
#
# (c) Régis FLORET 2013 and later - All right reserved
#

from tornado.web import RequestHandler
from App.models.preference import PreferenceModel


class CodesHandler(RequestHandler):
    """
    Handle all codes for analytics or captcha, twitter,
    """
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

    def post(self):
        """
        Save the codes
        """
        PreferenceModel().save_codes(
            analytics=self.get_argument('analytics'),
            recaptcha_private=self.get_argument('recapatcha_private'),
            recaptcha_private=self.get_argument('recapatcha_public'),
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