#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from handlers.base import MainHandler, CookieAlertHandler, AboutHandler
from handlers.topics import TopicAdd, TopicDetails, DeleteTopicHandler
from workers.email_comment_worker import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set_cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
    webapp2.Route('/topic/details/<topic_id:\d+>/delete', DeleteTopicHandler),
    # background tasks
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker)
], debug=True)
