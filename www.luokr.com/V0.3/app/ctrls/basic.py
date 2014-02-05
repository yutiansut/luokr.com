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
        self.store = {'model': {}, 'dbase': {}, }
    def on_finish(self):
        for dbase in self.store['dbase']:
            self.store['dbase'][dbase].close()

    def head(self, *args, **kwargs):
        apply(self.get, args, kwargs)
    def hello_world(self):
        self.write('Hello world')
    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            return self.render('404.html')

        if not self.settings['error']:
            return self.render('5xx.html')
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
        if 'admin' not in self.store:
            self.store['admin'] = None
            sess = self.get_current_user()
            if sess:
                user = self.model('admin').get_user_by_usid(self.dbase('users'), sess['user_id'])
                if user:
                    self.store['admin'] = user
                else:
                    self.del_current_user()

        if need:
            assert self.store['admin'] is not None
        return self.store['admin']
    def store_admin(self, user):
        self.store['admin'] = user

    def merge_query(self, args, base = '?'):
        for k in self.request.arguments.keys():
            if k not in args:
                args[k] = self.get_argument(k)
        return args

    def get_escaper(self):
        return tornado.escape

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
        if name not in self.store['dbase']:
            self.store['dbase'][name] = sqlite3.connect(self.settings['dbase'][name])
            self.store['dbase'][name].row_factory = sqlite3.Row
            self.store['dbase'][name].text_factory = str
        return self.store['dbase'][name]

    def model(self, name):
        name = name.title() + 'Model'
        if name not in self.store['model']:
            self.store['model'][name] = globals()[name]()
        return self.store['model'][name]
