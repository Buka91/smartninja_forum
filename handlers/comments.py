#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from utils.special_functions import is_local, check_csrf_protection
from handlers.base import BaseHandler
from models.comment import Comment


class DeleteCommentHandler(BaseHandler):

    @check_csrf_protection
    def post(self, comment_id):
        current_comment = Comment.get_by_id(int(comment_id))
        current_comment.deleted = True
        current_comment.put()

        topic_id = current_comment.topic_id

        if is_local():
            time.sleep(0.1)
        return self.redirect_to("topic-details", topic_id = int(topic_id))