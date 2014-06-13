#coding=utf-8

from basic import alive, BasicCtrl

class PanelCtrl(BasicCtrl):
    @alive
    def get(self, *args):
        user = self.current_user

        cur = self.dbase('alogs').cursor()
        cur.execute('select * from alogs where user_id=? order by alog_id desc limit 5', (user['user_id'], ))
        logs = cur.fetchall()
        cur.close()

        self.render('panel.html', user = user, logs = logs)

    @alive
    def post(self, *args):
        try:
            user = self.current_user

            user_name = self.input('name')
            user_mail = self.input('mail')
            user_pswd = self.input('pswd', None)
            user_npwd = self.input('npwd', None)
            user_rpwd = self.input('rpwd', None)

            if (not user_name) or (not user_mail):
                self.flash(0)
                return

            con = self.dbase('users')
            cur = con.cursor()
            if user_pswd:
                if len(user_npwd) < 6 or (not user_npwd == user_rpwd) or (not self.model('admin').generate_password(user_pswd, user['user_salt']) == user['user_pswd']):
                    self.flash(0, {'msg': '密码输入错误'})
                    return

                user_salt = self.model('admin').generate_randsalt(self.utils().str_md5(user_npwd))
                cur.execute('update users set user_name = ?, user_mail = ?, user_pswd = ?, user_salt = ?, user_atms = ?, user_utms = ? where user_id = ?',\
                        (user_name, user_mail, self.model('admin').generate_password(user_npwd, user_salt), user_salt, self.stime(), self.stime(), user['user_id'], ))
                con.commit()
            else:
                cur.execute('update users set user_name = ?, user_mail = ?, user_utms = ? where user_id = ?',\
                        (user_name, user_mail, self.stime(), user['user_id'], ))
                con.commit()

            cur.close()
            if (cur.rowcount):
                self.model('alogs').add(self.dbase('alogs'), '更新个人资料', user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1, {'msg': '更新资料成功', 'url': '/panel'})
                return
        except:
            pass
        self.flash(0)
