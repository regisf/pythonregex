
__author__ = 'Régis FLORET'


from App.models.regex import RegexModel
from tornadoext.requesthandler import RequestHandler
from tornado.web import authenticated


class AccountRegexHandler(RequestHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.render(
            "regex.html",
            regex=RegexModel().get_all_for_user(self.current_user)
        )

    @authenticated
    def delete(self, *args, **kwargs):
        print(self.get_argument('id', None))
        pass

