#coding=utf-8

import os, sys, hashlib
from admin import admin, AdminCtrl

class Admin_ImageUploadCtrl(AdminCtrl):
    def check_xsrf_cookie(self):
        return True

    @admin
    def post(self):
        if ('upload' in self.request.files) and (len(self.request.files['upload'])):
            ets = {'jpeg': 'jpg', 'jpg': 'jpg', 'png': 'png', 'gif': 'gif'}

            img = self.request.files['upload'][0]
            if img['content_type'].find('image/') == 0:
                ext = img['content_type'].split('/')[1]
                if ext in ets:
                    ext = ets[ext]
                    md5 = hashlib.md5()
                    md5.update(img['body'])
                    key = md5.hexdigest()
                    
                    url = '/upload/' + self.timer().strftime('%Y/%m/%d') + '/' + key[15] + key[16] + '/' + key[0] + key[1] + key[30] + key[31] + '/' + key + '.' + ext
                    uri = self.settings['apath'] + '/www' + url

                    if not os.path.exists(os.path.dirname(uri)):
                        os.makedirs(os.path.dirname(uri), mode=0777)

                    fin = open(uri, 'w')
                    fin.write(img['body'])
                    fin.close()

                    msg = ''
                    res = '<script type="text/javascript">'
                    res += 'window.parent.CKEDITOR.tools.callFunction(%s,"%s","%s");' % (self.input('CKEditorFuncNum'), url, msg)
                    res += '</script>'

                    self.write(res)
