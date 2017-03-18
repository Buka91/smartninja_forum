#!/usr/bin/env python
# -*- coding: utf-8 -*-

from handlers.base import BaseHandler
from google.appengine.api import mail # za pošiljanje mailov

class EmailNewCommentWorker(BaseHandler):
    def post(self): # worker ima vedno le POST metodo, nima GET metode; načeloma je to handler

        topic_author_email = self.request.get("topic_author_email")
        topic_title = self.request.get("topic_title")
        comment_content = self.request.get("comment_content")
        topic_id = self.request.get("topic_id")
        message = mail.EmailMessage(sender = "david.bukovsek@gmail.com",
                                    subject = "Dobil/a si nov komentar v topicu %s!" % topic_title)
        message.to = topic_author_email
        message.body = u"Nov komentar: {0}. Povezava: http://useful-ward-147715.appspot.com/topic/details/{1}".format(comment_content, topic_id)
        message.send()
        #mail.send_mail(sender = "david.bukovsek@gmail.com", to = topic_author_email,
        #               subject = "Dobil/a si nov komentar v topicu %s!" % topic_title,
        #               body = u"Nov komentar: {0}. Povezava: http://useful-ward-147715.appspot.com/topic/details/{1}".format(comment_content, topic_id))