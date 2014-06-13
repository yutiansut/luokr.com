#coding=utf-8

import functools

from app.ctrls.basic import alive, BasicCtrl

class AdminCtrl(BasicCtrl):
    pass

def admin(method):
    @alive
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.model('admin').chk_user_is_root(self.current_user):
            return method(self, *args, **kwargs)
        else:
            if ('Accept' in self.request.headers) and (self.request.headers['Accept'].find('json') >= 0):
                self.flash(0, {'url': self.get_login_url(), 'sta': 403})
                return
            return self.send_error(403)
    return wrapper
