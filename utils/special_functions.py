#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from google.appengine.api import memcache

def is_local():
    if os.environ.get('SERVER_NAME', '').startswith('localhost'):
        return True
    elif 'development' in os.environ.get('SERVER_SOFTWARE', '').lower():
        return True
    else:
        return False


def check_csrf_protection(handler):
    def func_wrapper(self, *args, **kwargs):
        csrf_token = self.request.get("csrf_token")
        mem_value = memcache.get(csrf_token)  # find if this CSRF exists in memcache

        if mem_value:
            return handler(self, *args, **kwargs)
        else:
            return self.write("You are hacker!")

    return func_wrapper

