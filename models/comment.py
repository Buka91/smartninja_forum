#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from google.appengine.api import taskqueue

class Comment(ndb.Model):
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    topic_id = ndb.IntegerProperty()
    topic_title = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, content, author, topic_id, topic):
        new_comment = cls(content = content, author_email = author, topic_id = topic_id, topic_title = topic.title)
        new_comment.put()
        #mail.send_mail(sender = "david.bukovsek@gmail.com", to = author,
        #               subject = "Dobil/a si nov komentar v topicu %s!" % topic.title,
        #               body = u"Nov komentar: {0}. Povezava: http://useful-ward-147715.appspot.com/topic/details/{1}".format(content, topic_id))
        taskqueue.add(url = "/task/email-new-comment", params = {"topic_author_email": author, "topic_title": topic.title,
                                                                 "comment_content": content, "topic_id": topic_id})

        return new_comment
