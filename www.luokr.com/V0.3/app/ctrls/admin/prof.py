#coding=utf-8

from admin import alive, AdminCtrl

class Admin_ProfCtrl(AdminCtrl):
    @alive
    def get(self, *args):
        user = self.fetch_admin()
        self.render('admin/prof.html', user = user)

    @alive
    def post(self, *args):
        try:
            user = self.fetch_admin()

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

                cur.execute('update users set user_name = ?, user_mail = ?, user_pswd = ?, user_utms = ? where user_id = ?',\
                        (user_name, user_mail, self.model('admin').generate_password(user_npwd, user['user_salt']), self.stime(), user['user_id'], ))
                con.commit()
            else:
                cur.execute('update users set user_name = ?, user_mail = ?, user_utms = ? where user_id = ?',\
                        (user_name, user_mail, self.stime(), user['user_id'], ))
                con.commit()

            cur.close()
            if (cur.rowcount):
                self.del_current_user()
                self.flash(1, {'msg': '更新资料成功，请重新登录', 'url': '/admin'})
                self.model('alogs').add(self.dbase('alogs'), '更新个人资料', user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                return
        except:
            pass
        self.flash(0)
