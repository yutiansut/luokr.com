#coding=utf-8

from shell import shell, ShellCtrl

class Shell_PanelCtrl(ShellCtrl):
    @shell
    def get(self, *args):
        user = self.current_user
        self.render('shell/panel.html', user = user)

    @shell
    def post(self, *args):
        try:
            user = self.current_user

            user_mail = self.input('mail')
            user_sign = self.input('sign', '')
            user_pswd = self.input('pswd', None)
            user_npwd = self.input('npwd', None)
            user_rpwd = self.input('rpwd', None)

            if not user_mail:
                self.flash(0)
                return

            con = self.dbase('users')
            cur = con.cursor()
            if user_pswd:
                if len(user_npwd) < 6 or user_npwd != user_rpwd or self.model('admin').generate_password(user_pswd, user['user_salt']) != user['user_pswd']:
                    self.flash(0, {'msg': '密码输入错误'})
                    return

                user_auid = self.model('admin').generate_randauid()
                user_salt = self.model('admin').generate_randsalt()
                cur.execute('update users set user_auid = ?, user_mail = ?, user_sign = ?, user_pswd = ?, user_salt = ?, user_atms = ?, user_utms = ? where user_id = ?',\
                        (user_auid, user_mail, user_sign, self.model('admin').generate_password(user_npwd, user_salt), user_salt, self.stime(), self.stime(), user['user_id'], ))
                con.commit()
            else:
                cur.execute('update users set user_mail = ?, user_sign = ?, user_utms = ? where user_id = ?',\
                        (user_mail, user_sign, self.stime(), user['user_id'], ))
                con.commit()

            cur.close()
            if (cur.rowcount):
                self.model('alogs').add(self.dbase('alogs'), '更新账号信息', user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1, {'msg': '更新成功'})
                return
        except:
            pass
        self.flash(0)
