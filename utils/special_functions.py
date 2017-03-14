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


# def check_csrf_protection(func):
#     def func_wrapper(some_object):
#         csrf_token = self.request.get("csrf_token") # to je vrednost v skritem input polju
#         csrf_value = memcache.get(csrf_token) # dobimo uporabnikov email
#         if str(csrf_value) != user.email(): # trenutni email in email v csrf_value se morata ujemati
#             return self.write("You are hacker!")

# def check_csrf_protection(user):
#     def tags_decorator(func):
#         def func_wrapper(self):
#             csrf_token = self.request.get("csrf_token")  # to je vrednost v skritem input polju
#             csrf_value = memcache.get(csrf_token)  # dobimo uporabnikov email
#             if str(csrf_value) != user.email():  # trenutni email in email v csrf_value se morata ujemati
#                 return self.write("You are hacker!")
#         return func_wrapper
#     return tags_decorator



def check_csrf_protection(handler):
    def func_wrapper(self, *args, **kwargs):
        csrf_token = self.request.get("csrf_token")
        mem_value = memcache.get(csrf_token)  # find if this CSRF exists in memcache

        if mem_value:
            return handler(self, *args, **kwargs)
        else:
            return self.write("You are hacker!")

    return func_wrapper

