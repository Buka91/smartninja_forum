#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest
import webapp2
import webtest
import uuid
import datetime

from google.appengine.ext import testbed
from google.appengine.api import memcache
from handlers.comments import DeleteCommentHandler
from handlers.topics import TopicDetails
from crons.delete_comment_cron import DeleteCommentCron
from models.topic import Topic
from models.comment import Comment


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
                webapp2.Route('/topic/details/<comment_id:\d+>/deleteComment', DeleteCommentHandler),
                webapp2.Route('/cron/delete-comment', DeleteCommentCron, name="cron-delete-comment"),
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub() # za uporabo memcache
        #self.testbed.init_mail_stub() # za pošiljanje mailov
        self.testbed.init_taskqueue_stub() # za background taske
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_post_comment_delete_handler(self):
        #POST
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com')
        topic.put()
        topic_query = Topic.query().get()
        self.assertTrue(topic_query)

        comment = Comment.create("That is my comment!", 'some.user@example.com', int(topic.key.id()), topic)
        comment_query = Comment.query().get()
        self.assertTrue(comment_query)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        params = {"csrf_token": csrf_token}
        post = self.testapp.post('/topic/details/{0}/deleteComment'.format(comment.key.id()), params = params)
        self.assertEqual(post.status_int, 302)

        comment_query_deleted = Comment.query().get()
        self.assertTrue(comment_query_deleted.deleted)

    def test_delete_comment_cron_handler(self):
        # GET
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com')
        topic.put()
        topic_query = Topic.query().get()
        self.assertTrue(topic_query)

        comment = Comment(content = "That is my comment!", author_email = 'some.user@example.com',
                          topic_id = int(topic.key.id()), topic_title = topic.title,
                          created = datetime.datetime.now() - datetime.timedelta(days = 32),
                          updated = datetime.datetime.now() - datetime.timedelta(days = 31),
                          deleted = True)
        comment.put()
        comment_query = Comment.query().get()
        self.assertTrue(comment_query)

        get = self.testapp.get('/cron/delete-comment')
        self.assertEqual(get.status_int, 200)