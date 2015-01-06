#coding=utf-8

import time
import functools
import threading
import tornado.web, tornado.httputil, tornado.escape
import sqlite3

try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3

try:
    from urllib import urlencode  # py2
except ImportError:
    from urllib.parse import urlencode  # py3

from lib.cache import Cache
from lib.mailx import Mailx
from lib.utils import Utils
from app.model.admin import AdminModel
from app.model.alogs import AlogsModel
from app.model.confs import ConfsModel
from app.model.posts import PostsModel

class BasicCtrl(tornado.web.RequestHandler):
    def initialize(self):
        self._storage = {'model': {}, 'dbase': {}, }
    def on_finish(self):
        for dbase in self._storage['dbase']:
            self._storage['dbase'][dbase].close()

    def set_default_headers(self):
        self.clear_header('server')
        self.set_header('x-frame-options', 'SAMEORIGIN')
        self.set_header('x-xss-protection', '1; mode=block')
        self.set_header('cache-control', 'no-transform')

    def head(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def write_error(self, status_code, **kwargs):
        if not self.settings['error']:
            self.flash(0, {'sta': status_code})
            return
        return super(BasicCtrl, self).write_error(*[status_code], **kwargs)

    def get_runtime_conf(self, name, json = False):
        if json:
            conf = self.model('confs').get(self.dbase('confs'), name)
            if conf is None or conf == '':
                return None
            return self.get_escaper().json_decode(conf)
        return self.model('confs').get(self.dbase('confs'), name)

    def has_runtime_conf(self, name):
        return self.model('confs').has(self.dbase('confs'), name)

    def del_runtime_conf(self, name):
        return self.model('confs').delete(self.dbase('confs'), name)

    def set_runtime_conf(self, name, vals):
        return self.model('confs').set(self.dbase('confs'), name, vals)

    def get_current_user(self):
        usid = self.get_cookie("_usid")
        auid = self.get_secure_cookie('_auid')
        auth = self.get_secure_cookie('_auth')
        if usid and auth:
            user = self.model('admin').get_user_by_usid(self.dbase('users'), usid)
            if user and user['user_auid'] == auid and \
                    self.model('admin').generate_authword(user['user_atms'], user['user_salt']) == auth:
                return user
            self.del_current_sess()
    def del_current_sess(self):
        self.clear_cookie("_auid")
        self.clear_cookie("_auth")
        # self.clear_cookie("_usid")

    def merge_query(self, args, dels = []):
        for k in self.request.arguments.keys():
            if k not in args and k[0] != '_':
                args[k] = self.get_argument(k)
        for k in dels:
            if k in args:
                del args[k]
        return args

    def get_escaper(self):
        return tornado.escape

    def fetch_xsrfs(self):
        return '_xsrf=' + self.get_escaper().url_escape(self.xsrf_token)

    def human_valid(self):
        field = '_code'
        value = self.get_secure_cookie(field)
        if value:
            self.clear_cookie(field)
            input = self.input(field, None)
            if input:
                value = self.get_escaper().json_decode(value)
                return 'time' in value and 'code' in value\
                        and 0 < self.stime() - value['time'] < 60\
                        and value['code'] == self.utils().str_md5(\
                        self.utils().str_md5(self.settings['cookie_secret']) + input.lower() + str(value['time']))
        return False

    def utils(self):
        return Utils

    def cache(self):
        return Cache

    def timer(self):
        return time

    def stime(self):
        return int(time.time())

    def tourl(self, args, base = None):
        if base == None:
            base = self.request.path
        return tornado.httputil.url_concat(base, args)

    def input(self, *args, **kwargs):
        return self.get_argument(*args, **kwargs)

    def email(self, *args, **kwargs):
        conf = self.get_runtime_conf('mailx', json = True)
        if conf and 'smtp_able' in conf and conf['smtp_able']:
            threading.Thread(target=Mailx(conf).send, args = args, kwargs = kwargs).start()

    def flash(self, isok, exts = {}):
        if isok:
            exts['err'] = 0
        else:
            exts['err'] = 1

        if 'sta' in exts:
            self.set_status(exts['sta'])
        else:
            exts['sta'] = self.get_status()

        if 'msg' not in exts:
            exts['msg'] = self._reason

        if 'url' not in exts: exts['url'] = ''
        if 'ext' not in exts: exts['ext'] = {}

        if ('Accept' in self.request.headers) and (self.request.headers['Accept'].find('json') >= 0):
            self.write(self.get_escaper().json_encode(exts))
        else:
            self.render('flash.html', flash = exts)

    def dbase(self, name):
        if name not in self._storage['dbase']:
            self._storage['dbase'][name] = sqlite3.connect(self.settings['dbase'][name])
            self._storage['dbase'][name].row_factory = sqlite3.Row
            self._storage['dbase'][name].text_factory = str
        return self._storage['dbase'][name]

    def model(self, name):
        name = name.title() + 'Model'
        if name not in self._storage['model']:
            self._storage['model'][name] = globals()[name]()
        return self._storage['model'][name]

def alive(method):
    """Decorate methods with this to require that the user be logged in.

    If the user is not logged in, they will be redirected to the configured
    `login url <RequestHandler.get_login_url>`.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if ('Accept' in self.request.headers) and (self.request.headers['Accept'].find('json') >= 0):
                self.flash(0, {'sta': 403, 'url': self.get_login_url()})
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
            self.flash(0, {'sta': 403})
            return
        return method(self, *args, **kwargs)
    return wrapper
