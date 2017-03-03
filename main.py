#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from handlers.base import MainHandler
from handlers.base import CookieAlertHandler
from handlers.base import AboutHandler
from handlers.topics import TopicAdd
from handlers.topics import TopicDetails

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set_cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details")
], debug=True)
