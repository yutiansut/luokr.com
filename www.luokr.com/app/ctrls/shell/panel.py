#coding=utf-8

import os, hashlib, mimetypes
from shell import shell, ShellCtrl

class Shell_PanelCtrl(ShellCtrl):
    @shell
    def get(self, *args):
        self.render('shell/panel.html', user = self.current_user)

    @shell
    def post(self, *args):
        try:
            user = self.current_user

            user_mail = self.input('mail')
            user_sign = self.input('sign', '')
            user_meta = self.input('meta', '')
            user_pswd = self.input('pswd', None)
            user_npwd = self.input('npwd', None)
            user_rpwd = self.input('rpwd', None)

            if not user_mail:
                self.flash(0)
                return

            if len(user_mail) < 3 or not self.model('admin').chk_is_user_mail(user_mail):
                self.flash(0, {'msg': '无效的用户邮箱'})
                return

            if user_mail != user['user_mail'] and self.model('admin').get_user_by_mail(self.datum('users'), user_mail):
                self.flash(0, {'msg': '用户邮箱已存在'})
                return

            user_logo = user['user_logo']
            if 'logo' in self.request.files and len(self.request.files['logo']) > 0:
                res = self.request.files['logo'][0]

                if 'content_type' not in res or res['content_type'].find('/') < 1 or len(res['content_type']) > 128:
                    self.flash(0, {'msg': '文件类型错误'})
                    return

                if 'filename' not in res or res['filename'] == '':
                    self.flash(0, {'msg': '文件名称错误'})
                    return

                ets = mimetypes.guess_all_extensions(res['content_type'])
                ext = os.path.splitext(res['filename'])[1].lower()
                if ets and ext not in ets:
                    ext = ets[0]

                ets = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
                if ext not in ets:
                    self.flash(0, {'msg': '文件类型受限'})
                    return

                md5 = hashlib.md5()
                md5.update(res['body'])
                key = md5.hexdigest()

                dir = '/www'
                url = '/upload/' + self.timer().strftime('%Y/%m/%d/') + key[0] + key[1] + key[30] + key[31] + '/' + key + ext
                uri = self.settings['root_path'] + dir + url

                if not os.path.exists(os.path.dirname(uri)):
                    os.makedirs(os.path.dirname(uri), mode=0777)

                fin = open(uri, 'w')
                fin.write(res['body'])
                fin.close()

                self.datum('files').affect('insert into files (file_hash, file_base, file_path, file_type, file_memo, file_ctms) values (?, ?, ?, ?, ?, ?)',
                        (key, dir, url, res['content_type'], res['filename'], self.stime()))

                user_logo = url

            if user_pswd:
                if len(user_npwd) < 6 or user_npwd != user_rpwd or self.model('admin').generate_password(user_pswd, user['user_salt']) != user['user_pswd']:
                    self.flash(0, {'msg': '密码输入错误'})
                    return

                user_auid = self.model('admin').generate_randauid()
                user_salt = self.model('admin').generate_randsalt()
                self.datum('users').affect(
                        'update users set user_auid = ?, user_mail = ?, user_logo = ?, user_sign = ?, user_meta = ?, user_pswd = ?, user_salt = ?, user_atms = ?, user_utms = ? where user_id = ?',
                        (user_auid, user_mail, user_logo, user_sign, user_meta, self.model('admin').generate_password(user_npwd, user_salt), user_salt, self.stime(), self.stime(), user['user_id'], ))
            else:
                self.datum('users').affect(
                        'update users set user_mail = ?, user_logo = ?, user_sign = ?, user_meta = ?, user_utms = ? where user_id = ?',
                        (user_mail, user_logo, user_sign, user_meta, self.stime(), user['user_id'], ))

            self.ualog(self.current_user, '更新账号信息')
            self.flash(1, {'msg': '更新成功'})
            return
        except:
            pass
        self.flash(0)
