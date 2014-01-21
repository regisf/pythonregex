from tornado.web import RequestHandler

__author__ = 'Regis FLORET'


class Admin(RequestHandler):
    """

    """

    def create(self):
        """ Create the email """
        raise NotImplementedError()

    def read(self):
        """ Read the whole list """
        raise NotImplementedError()

    def update(self, value):
        """ Update a particular user """
        raise NotImplementedError()

    def delete(self, value):
        """ Delete the user """
        raise NotImplementedError()
