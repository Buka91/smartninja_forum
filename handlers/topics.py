#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils.special_functions import is_local, check_csrf_protection
from handlers.base import BaseHandler
from models.topic import Topic
from models.comment import Comment
from models.users import User
from google.appengine.api import users
import time

class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    @check_csrf_protection
    def post(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        title = self.request.get("title")
        text = self.request.get("text")

        new_topic = Topic.create(title, text, user)

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id = new_topic.key.id())


class TopicDetails(BaseHandler):
    def get(self, topic_id):
        topic = Topic.get_by_id(int(topic_id))
        comments = Comment.query().filter(Comment.topic_id == int(topic_id), Comment.deleted == False).fetch()
        params = {"topic": topic, "comments": comments}
        return self.render_template("topic_details.html", params = params)

    @check_csrf_protection
    def post(self, topic_id):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you comment on topic!")

        # CSRF protection
        #csrf_token = self.request.get("csrf_token")
        #csrf_value = memcache.get(csrf_token)
        #if str(csrf_value) != user.email():
        #    return self.write("You are hecker!")

        current_topic = Topic.get_by_id(int(topic_id))
        content = self.request.get("get_comment")

        Comment.create(content, user.email(), int(topic_id), current_topic)

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id = int(topic_id))


class DeleteTopicHandler(BaseHandler):

    @check_csrf_protection
    def post(self, topic_id):
        current_topic = Topic.get_by_id(int(topic_id))
        current_topic.deleted = True
        current_topic.put()

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("main-page")


class HottestTopicHandler(BaseHandler):

    @check_csrf_protection
    def post(self):
        user_email = self.request.get("email")
        User.get_or_create(email = user_email)

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("main-page")