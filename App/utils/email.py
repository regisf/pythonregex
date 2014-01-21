"""
Email utils
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail(sender, dest, subject, body, host_pref={'server': 'localhost'}):
    """
    Send an email with HTML content
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = dest

    html_part = MIMEText(body, 'html')
    msg.attach(html_part)

    s = smtplib.SMTP(host_pref['server'])
    s.send_message(msg)
    s.quit()

