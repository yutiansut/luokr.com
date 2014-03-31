#coding=utf-8

import functools
import tornado.web
from tornado import escape
from tornado import httputil

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

def alive(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if ('Accept' in self.request.headers) and (self.request.headers['Accept'].find('json') >= 0):
                self.flash(0, {'url': self.get_login_url(), 'msg': '403 Forbidden!'})
                return

            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                        if next_url.find('/index.py') == 0:
                            next_url = next_url.replace('/index.py', '', 1)

                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            return self.send_error(403)
        return method(self, *args, **kwargs)
    return wrapper


from app.ctrls.basic import BasicCtrl

class AdminCtrl(BasicCtrl):
    def get(self):
        return self.send_error(404)
    def post(self):
        return self.send_error(404)
