# encoding: utf-8

import web.core
import web.auth

from marrow.util.bunch import Bunch



class LoginMethod(web.core.HTTPMethod):
    def get(self, redirect=None):
        if redirect is None:
            referrer = web.core.request.referrer
            redirect = '/' if referrer.endswith(web.core.request.script_name) else referrer
        
        return "quorum.templates.authenticate", dict(redirect=redirect, user=None)
    
    def post(self, **data):
        data = Bunch(data)
        
        if not web.auth.authenticate(data.user, data.password):
            web.session['flash'] = "Authentication failure."
            return "quorum.templates.authenticate", dict(redirect=data.redirect, user=data.user)
        
        if data.redirect:
            raise web.core.http.HTTPFound(location=data.redirect)
        
        raise web.core.http.HTTPFound(location='/')


class AuthenticationMixIn(object):
    authenticate = LoginMethod()
    
    def depart(self):
        web.auth.deauthenticate()
        raise web.core.http.HTTPFound(location='/')
