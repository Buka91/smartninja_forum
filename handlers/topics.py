#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers.base import BaseHandler, is_local
from models.topic import Topic
from models.comment import Comment
from google.appengine.api import users, memcache
import time

class TopicAdd(BaseHandler):
    def get(self):
        return self.render_template("topic_add.html")

    def post(self):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you're allowed to post a topic.")

        # CSRF protection
        csrf_token = self.request.get("csrf_token") # to je vrednost v skritem input polju
        csrf_value = memcache.get(csrf_token) # dobimo uporabnikov email
        if str(csrf_value) != user.email(): # trenutni email in email v csrf_value se morata ujemati
            return self.write("You are hacker!")

        title = self.request.get("title")
        text = self.request.get("text")

        #new_topic = Topic(title=title, content=text, author_email=user.email())
        #new_topic.put()  # put() saves the object in Datastore
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

    def post(self, topic_id):
        user = users.get_current_user()

        if not user:
            return self.write("Please login before you comment on topic!")

        # CSRF protection
        csrf_token = self.request.get("csrf_token")
        csrf_value = memcache.get(csrf_token)
        if str(csrf_value) != user.email():
            return self.write("You are hecker!")

        current_topic = Topic.get_by_id(int(topic_id))
        content = self.request.get("get_comment") #.encode("utf-8")

        Comment.create(content, user.email(), int(topic_id), current_topic)

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id = int(topic_id))


class DeleteTopicHandler(BaseHandler):
    def post(self, topic_id):
        current_topic = Topic.get_by_id(int(topic_id))
        current_topic.deleted = True
        current_topic.put()

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("main-page") #, params = params)

