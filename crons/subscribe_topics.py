#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from handlers.base import BaseHandler
from models.topic import Topic
from models.users import User
from google.appengine.api import mail

class EmailHottestTopicCron(BaseHandler):
    def get(self):
        hottest_topics = Topic.query(Topic.updated > datetime.datetime.now() - datetime.timedelta(hours = 24)).fetch()
        topics = ""
        for hot_topic in hottest_topics:
            if hot_topic.title:
                topics += (hot_topic.title + ", ")
        users = User.query(User.subscribed == True).fetch()
        if users:
            for usr in users:
                message = mail.EmailMessage(sender = "david.bukovsek@gmail.com",
                                            subject = u"Seznam najbolj vročih topicov")
                message.to = usr.email
                message.body = u"Naslednji topici so bili posodobljeni v zadnjih 24 urah: %s" %topics[:-2]
                message.send()
                #mail.send_mail(sender = "david.bukovsek@gmail.com", to = usr.email,
                #               subject = u"Seznam najbolj vročih topicov",
                #               body = u"Naslednji topici so bili posodobljeni v zadnjih 24 urah: %s" %topics[:-2])