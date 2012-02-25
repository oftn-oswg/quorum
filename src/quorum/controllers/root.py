# encoding: utf-8

import web.core
import web.auth

from web.core import Controller

from quorum.controllers.auth import AuthenticationMixIn



class RootController(Controller, AuthenticationMixIn):
    def index(self):
        """Present anonymous users with a welcome page, redirect authenticated users to the issue list."""
        if web.auth.authenticated:
            raise web.core.http.HTTPFound(location='/issues')
        
        return 'quorum.templates.master', dict()
