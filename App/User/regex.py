
__author__ = 'Régis FLORET'


from tornadoext.requesthandler import RequestHandler


class AccountRegexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("regex.html")
