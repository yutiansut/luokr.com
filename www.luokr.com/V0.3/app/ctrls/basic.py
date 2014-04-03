#coding=utf-8

import time
import tornado.web, tornado.httputil, tornado.escape
import sqlite3

from lib.cache import Cache
from lib.utils import Utils
from lib.recaptcha.client.captcha import submit
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

    def head(self, *args, **kwargs):
        apply(self.get, args, kwargs)
    def hello_world(self):
        self.write('Hello world')
    def write_error(self, status_code, **kwargs):
        if not self.settings['error']:
            return self.render('error.html', code = status_code, msgs = self._reason)
        return apply(super(BasicCtrl, self).write_error, [status_code], kwargs)

    def get_runtime_conf(self, name):
        return self.model('confs').get(self.dbase('confs'), name)

    def has_runtime_conf(self, name):
        return self.model('confs').has(self.dbase('confs'), name)

    def del_runtime_conf(self, name):
        return self.model('confs').delete(self.dbase('confs'), name)

    def set_runtime_conf(self, name, vals):
        return self.model('confs').set(self.dbase('confs'), name, vals)

    def get_current_user(self):
        sess = self.get_secure_cookie("_user")
        if (sess):
            return self.get_escaper().json_decode(sess)

    def del_current_user(self):
        self.clear_cookie("_user")

    def fetch_admin(self, need = True):
        if 'admin' not in self._storage:
            self._storage['admin'] = None
            sess = self.get_current_user()
            if sess:
                user = self.model('admin').get_user_by_usid(self.dbase('users'), sess['user_id'])
                if user:
                    self._storage['admin'] = user
                else:
                    self.del_current_user()

        if need:
            assert self._storage['admin'] is not None
        return self._storage['admin']
    def store_admin(self, user):
        self._storage['admin'] = user

    def merge_query(self, args, base = '?'):
        for k in self.request.arguments.keys():
            if k not in args:
                args[k] = self.get_argument(k)
        return args

    def get_escaper(self):
        return tornado.escape

    def fetch_xsrfs(self):
        return '_xsrf=' + self.get_escaper().url_escape(self.xsrf_token)

    def human_valid(self):
        if self.get_runtime_conf('rapri'):
            return submit(self.input('recaptcha_challenge_field', None), self.input('recaptcha_response_field', None), \
                    self.get_runtime_conf('rapri'), self.request.remote_ip).is_valid
        else:
            return not bool(self.get_runtime_conf('rapub'))

    def utils(self):
        return Utils

    def cache(self):
        return Cache

    def timer(self):
        return time

    def stime(self):
        return int(time.time())

    def tourl(self, args, base = '?'):
        return tornado.httputil.url_concat(base, args)

    def input(self, *args, **kwargs):
        return apply(self.get_argument, args, kwargs)

    def flash(self, stat, exts = {}):
        if stat:
            exts['err'] = 0
        else:
            exts['err'] = 1
        if 'msg' not in exts: exts['msg'] = ''
        if 'url' not in exts: exts['url'] = ''
        if 'ext' not in exts: exts['ext'] = {}

        if ('Accept' in self.request.headers) and (self.request.headers['Accept'].find('json') >= 0):
            self.write(self.get_escaper().json_encode(exts))
        else:
            self.render('flash.html', flash = exts)

    def confs(self):
        return self.model('confs')

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
