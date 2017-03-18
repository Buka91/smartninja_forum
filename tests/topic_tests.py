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
from handlers.topics import TopicAdd, TopicDetails, DeleteTopicHandler, HottestTopicHandler
from handlers.base import MainHandler
from crons.delete_topics_cron import DeleteTopicsCron
from crons.subscribe_topics import EmailHottestTopicCron
from models.topic import Topic
from models.comment import Comment
from models.users import User


class TopicTests(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication(
            [
                webapp2.Route('/', MainHandler, name="main-page"),
                webapp2.Route('/topic/add', TopicAdd, name="topic-add"),
                webapp2.Route('/topic/details/<topic_id:\d+>', TopicDetails, name="topic-details"),
                webapp2.Route('/topic/details/<topic_id:\d+>/delete', DeleteTopicHandler),
                webapp2.Route('/subscribe/hottest-topics', HottestTopicHandler),
                webapp2.Route('/cron/delete-topics', DeleteTopicsCron, name="cron-delete-topics"),
                webapp2.Route('/cron/email-subscribe', EmailHottestTopicCron)
            ])

        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

        """ Uncomment the stubs that you need to run tests. """
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub() # za uporabo memcache
        self.testbed.init_mail_stub() # za pošiljanje mailov
        self.testbed.init_taskqueue_stub() # za background taske
        self.testbed.init_user_stub()
        # ...

        """ Uncomment if you need user (Google Login) and if this user needs to be admin. """
        os.environ['USER_EMAIL'] = 'some.user@example.com'
        # os.environ['USER_IS_ADMIN'] = '1'

    def tearDown(self):
        self.testbed.deactivate()

    def test_add_topic_handler(self): # ime funkcije se mora začeti s test_...
        get = self.testapp.get('/topic/add')  # get add topic handler
        self.assertEqual(get.status_int, 200)  # if GET request was ok, it should return 200 status code
        self.assertIn("Add new topic", get.body) # preveri, ali se besede "Add new topic" nahajajo znotraj body-ja spletne strani

    def test_post_add_topic_handler(self):
        # POST
        title = "Moj testni topic"
        content = "bla bla bla"
        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)
        params = {"title": title, "text": content, "csrf_token": csrf_token}

        post = self.testapp.post("/topic/add", params = params)
        self.assertEqual(post.status_int, 302) # koda za uspešen redirect je 302

    def test_get_topic_details_handler(self):
        # GET
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com')
        topic.put()
        get = self.testapp.get('/topic/details/{0}'.format(topic.key.id()))
        self.assertEqual(get.status_int, 200)

    def test_post_topic_details_handler(self):
        # POST
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com')
        topic.put()
        topic_query = Topic.query().get()
        self.assertTrue(topic_query) # pošjem v bazo

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        comment_content = "That is my comment!"
        Comment.create(comment_content, 'some.user@example.com', int(topic.key.id()), topic)
        params = {"get_comment": comment_content, "csrf_token": csrf_token}
        post = self.testapp.post('/topic/details/{0}'.format(topic.key.id()), params = params)
        self.assertEqual(post.status_int, 302)

    def test_post_topic_delete_handler(self):
        #POST
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com')
        topic.put()
        topic_query = Topic.query().get()
        self.assertTrue(topic_query)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value='some.user@example.com', time=600)

        params = {"csrf_token": csrf_token}
        post = self.testapp.post('/topic/details/{0}/delete'.format(topic.key.id()), params = params)
        self.assertEqual(post.status_int, 302)

        topic_query_deleted = Topic.query().get()
        self.assertTrue(topic_query_deleted.deleted)

    def test_post_hottest_topic_handler(self):
        #POST
        user_email = 'some.user@example.com'
        User.get_or_create(email = user_email)

        csrf_token = str(uuid.uuid4())
        memcache.add(key=csrf_token, value=user_email, time=600)

        params = {"csrf_token": csrf_token, "email": user_email}
        post = self.testapp.post('/subscribe/hottest-topics', params = params)
        self.assertEqual(post.status_int, 302)

        user_query = User.query().get()
        self.assertTrue(user_query)

    def test_delete_topic_cron_handler(self):
        # GET
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com',
                      created = datetime.datetime.now() - datetime.timedelta(days = 32),
                      updated = datetime.datetime.now() - datetime.timedelta(days = 31),
                      deleted = True)
        topic.put()

        topic_query = Topic.query().get()
        self.assertTrue(topic_query)

        get = self.testapp.get('/cron/delete-topics')
        self.assertEqual(get.status_int, 200)

    def test_subscribe_hottest_topic_cron_handler(self):
        # GET
        topic = Topic(title = "New topic", content = "Content of new topic!", author_email = 'some.user@example.com',
                      created = datetime.datetime.now() - datetime.timedelta(days = 2),
                      updated = datetime.datetime.now() - datetime.timedelta(hours = 12),
                      deleted = True)
        topic.put()

        topic_query = Topic.query().get()
        self.assertTrue(topic_query)

        get = self.testapp.get('/cron/email-subscribe')
        self.assertEqual(get.status_int, 200)