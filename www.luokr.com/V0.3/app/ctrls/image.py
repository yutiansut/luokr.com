#coding=utf-8

from lib.captcha.image import gen_randoms, gen_captcha
from basic import BasicCtrl

class ImageRandomCtrl(BasicCtrl):
    def get(self):
        text = gen_randoms().strip()
        self.session['_code'] = text

        self.set_header('Content-Type', 'image/jpeg')
        self.write(gen_captcha(text, 'jpeg'))
