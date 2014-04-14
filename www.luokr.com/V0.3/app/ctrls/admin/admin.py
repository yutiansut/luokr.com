#coding=utf-8

import functools

from app.ctrls.basic import alive, BasicCtrl

class AdminCtrl(BasicCtrl):
    pass

def admin(method):
    @alive
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        return method(self, *args, **kwargs)
    return wrapper
