#coding=utf-8

from lib.captcha.image import gen_randoms, gen_captcha
from basic import BasicCtrl

class ImageRandomCtrl(BasicCtrl):
    def get(self):
        text = gen_randoms().strip()
        time = self.stime()
        self.set_secure_cookie('_code', self.get_escaper().json_encode(\
                dict(code=self.utils().str_md5(self.utils().str_md5(self.settings['cookie_secret']) + text.lower() + str(time)), time=time))\
                , expires_days = None)

        self.set_header('Content-Type', 'image/jpeg')
        self.write(gen_captcha(text, 'jpeg'))
