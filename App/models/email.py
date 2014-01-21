"""
Email model
"""

from . import database


class EmailModel:
    def __init__(self):
        self.email = database.email

    def get_template(self, shortcut):
        """
        Get a template from it's shortcut
        """
        template = self.email.find_one({'shortcut': shortcut})
        if template:
            return template.subject, template.body

        return None, None

    def shortcut_exists(self, name):
        """
        Test if a shortcut exists
        """
        return self.email.find_one({'shortcut': name}) is not None

    def find_by_shortcut(self, short):
        """ Find an email with its shortcut """
        return self.email.find_one({'shortcut': short})

    def all(self, ):
        """ Get all emails in database """
        return self.email.find()

    def delete(self, shortcut):
        """ Delete a particular email. The key is the shortcut """
        self.email.remove({'shortcut': shortcut})

    def add_email(self, title, shortcut, content):
        """ Add an email """
        self.email.insert({
            'title': title,
            'shortcut': shortcut,
            'content': content
        })

    def edit_email(self, previous_shortcut, title, shortcut, content):
        """ Update an entry """
        self.email.update(
            {'shortcut': previous_shortcut},
            {'$set': {'title': title, 'shortcut': shortcut, 'content': content}}
        )

    def set_host_preferences(self):
        """
        """

    def get_host_preferences(self):
        """
        Get the SMTP host preferences.
        Use default if there's not pref
        """
        pref = self.email.find_one()
        return {
            'host': pref.get('server', 'localhost'),

        }