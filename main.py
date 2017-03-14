#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2

from crons.delete_topics_cron import DeleteTopicsCron
from crons.subscribe_topics import EmailHottestTopicCron
from crons.delete_comment_cron import DeleteCommentCron
from handlers.base import MainHandler, CookieAlertHandler, AboutHandler
from handlers.topics import TopicAdd, TopicDetails, DeleteTopicHandler
from handlers.topics import HottestTopicHandler
from handlers.comments import DeleteCommentHandler
from workers.email_comment_worker import EmailNewCommentWorker

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main-page"),
    webapp2.Route('/set_cookie', CookieAlertHandler, name="set-cookie"),
    webapp2.Route('/about', AboutHandler, name="about-page"),
    webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
    webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
    webapp2.Route('/topic/details/<topic_id:\d+>/delete', DeleteTopicHandler),
    webapp2.Route('/subscribe/hottest-topics', HottestTopicHandler),
    webapp2.Route('/topic/details/<comment_id:\d+>/deleteComment', DeleteCommentHandler),
    # background tasks
    webapp2.Route('/task/email-new-comment', EmailNewCommentWorker),
    # cron jobs
    webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name="cron-delete-topics"),
    webapp2.Route('/cron/delete-comment', DeleteCommentCron, name="cron-delete-comment"),
    webapp2.Route('/cron/email-subscribe', EmailHottestTopicCron)
], debug=True)
