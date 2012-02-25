# encoding: utf-8

from web.core import Controller


class BaseController(Controller):
    def getattr(self, name):
        if name == 'index':
            