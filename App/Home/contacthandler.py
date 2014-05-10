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

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from tornado.web import RequestHandler

from App.models.email import  EmailModel
import private_settings

class ContactHandler(RequestHandler):
    """
    Send an email via the contact form
    """
    def post(self):
        """
        Manage post
        """
        email = self.get_argument('email')
        name = self.get_argument('name')
        question = self.get_argument('question')
        answer = self.get_argument('answer')
        message = self.get_argument('message')

        if email and name and question and answer and message and question == answer:
            """ Send mail"""
            try:
                model = EmailModel()
                # Contact email is the default
                if not model.shortcut_exists(getattr(private_settings, "CONTACT_EMAIL", "contact_email")):
                    self.write("The email preferences are not set")
                else:
                    # Replace all tags.
                    email_object = model.find_by_shortcut(private_settings.CONTACT_EMAIL)
                    email_pref = model.get_host_preferences()
                    content = email_object['content']
                    content = re.sub(r'\{\{[\s+|]sender[\s+|]\}\}', name, content)
                    content = re.sub(r'\{\{[\s+|]email[\s+|]\}\}', email, content)
                    content = re.sub(r'\{\{[\s+|]message[\s+|]\}\}', message, content)
                    content = re.sub(r'\{\{[\s+|].*?[\s+|]\}\}', '', content)

                    # Simply convert HTML to text
                    text_content = re.sub(r'<p>(.*?)</p>', '\\1\n', content)

                    msg = MIMEMultipart('alternative')
                    part1 = MIMEText(text_content, 'plain')
                    part2 = MIMEText(content, 'html')
                    msg.attach(part1)
                    msg.attach(part2)

                    msg['Subject'] = email_object['title']
                    if 'mail_sender' in email_pref:
                        msg['From'] = email_pref['mail_sender']
                    else:
                        msg['From'] = getattr(private_settings, 'DEFAULT_EMAIL', "nobody@nowhere.tld")
                    msg['To'] = email_pref['mail_receiver']

                    smtp = smtplib.SMTP(email_pref['server'])
                    smtp.sendmail(getattr(private_settings, 'DEFAULT_EMAIL', "nobody@nowhere.tld"),
                                  email_pref['mail_receiver'], msg.as_string())
                    smtp.quit()

                    self.write("ok")
            except Exception as e:
                self.write("error: " + str(e))


