# -*- coding: utf-8 -*-

from tornado.web import UIModule


class SimpleDate(UIModule):
    def render(self, value, pattern=None, *args, **kwargs):
        """
        Transform datetime.datetime into a human readable date
        """
        try:
            if pattern:
                return value.strftime(pattern)
            return value
        except:
            pass

        return value