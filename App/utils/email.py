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
Email utils
"""

import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr

import html2text

import private_settings


def send_mail(sender, dest, subject, body, host_pref={'name': 'localhost'}):
    """
    Send an email with HTML content
    """
    if getattr(private_settings, "USE_EMAIL", False):
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = dest

        text_part = MIMEText(html2text.html2text(body), 'text')
        html_part = MIMEText(body, 'html')
        msg.attach(html_part)
        msg.attach(text_part)

        smtp = smtplib.SMTP(host_pref['name'])
        smtp.sendmail(
            getattr(private_settings, 'DEFAULT_EMAIL', "nobody@nowhere.tld"),
            dest,
            msg.as_string()
        )
        smtp.quit()

def is_email(email):
    """ Test if an email is valid
    """
    name, address = parseaddr(email)
    return True if address else False