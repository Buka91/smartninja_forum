#!/usr/bin/env python

from handlers import base

app = base.webapp2.WSGIApplication([
    base.webapp2.Route('/', base.MainHandler, name="main-page"),
    base.webapp2.Route('/set_cookie', base.CookieAlertHandler, name="set-cookie"),
    base.webapp2.Route('/about', base.AboutHandler, name="about-page")
], debug=True)
