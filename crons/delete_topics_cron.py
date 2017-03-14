#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from handlers.base import BaseHandler
from models.topic import Topic

# CRON JOB imajo samo GET metodo; namenjeni so avtomatizaciji procesov -> delujejo samodejno na vsake toliko časa
class DeleteTopicsCron(BaseHandler):
    def get(self):
        # zbrišemo vse topice, ki smo jih označili z DELETED pred več kot 30 dnevi
        deleted_topics = Topic.query(Topic.deleted == True,
                                     Topic.updated < datetime.datetime.now() - datetime.timedelta(days = 30)).fetch() # več kot en != ne sme obstajati v query-ju
        for topic in deleted_topics:
            topic.key.delete()
