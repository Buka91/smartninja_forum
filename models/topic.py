#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

class Topic(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    author_email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add = True) # čas ob ustvarjanju
    updated = ndb.DateTimeProperty(auto_now = True) # čas, ko se topic posodablja
    deleted = ndb.BooleanProperty(default = False)

    @classmethod
    def create(cls, title, text, user):
        new_topic = cls(title = title, content = text, author_email = user.email())
        new_topic.put()  # put() saves the object in Datastore
        return new_topic