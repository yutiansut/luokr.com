#coding=utf-8

from admin import admin, AdminCtrl

class Admin_UsersCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('users').cursor()
        cur.execute('select * from users order by user_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        users = cur.fetchall()
        cur.close()

        if users:
            pager['list'] = len(users)

        self.render('admin/users.html', users = users, pager = pager)

class Admin_UserCtrl(AdminCtrl):
    @admin
    def get(self):
        user = self.model('admin').get_user_by_usid(self.dbase('users'), self.input('user_id'))
        if not user:
            self.flash(0, {'sta': 404})
            return

        if user['user_id'] == self.current_user['user_id']:
            self.flash(0, {'sta': 403})
            return

        self.render('admin/user.html', user = user)

    @admin
    def post(self):
        user = self.model('admin').get_user_by_usid(self.dbase('users'), self.input('user_id'))
        if not user:
            self.flash(0, {'sta': 404})
            return

        if user['user_id'] == self.current_user['user_id']:
            self.flash(0, {'sta': 403})
            return

        try:
            user_mail = self.input('user_mail')
            user_sign = self.input('user_sign')
            user_logo = self.input('user_logo')
            user_perm = self.input('user_perm')
            user_pswd = self.input('user_pswd', '')
            user_rpwd = self.input('user_rpwd', '')
            user_perm = int(user_perm) & 0x7FFFFFFF
            
            con = self.dbase('users')
            cur = con.cursor()
            if user_pswd:
                if len(user_pswd) < 6 or (user_pswd != user_rpwd):
                    self.flash(0, {'msg': '无效的用户密码'})
                    return

                user_auid = self.model('admin').generate_randauid()
                user_salt = self.model('admin').generate_randsalt()
                user_pswd = self.model('admin').generate_password(user_pswd, user_salt)
                cur.execute('update users set user_auid = ?, user_mail = ?, user_sign = ?, user_logo = ?, user_pswd = ?, user_salt = ?, user_perm = ?, user_atms = ?, user_utms = ? where user_id = ?',\
                        (user_auid, user_mail, user_sign, user_logo, user_pswd, user_salt, user_perm, self.stime(), self.stime(), user['user_id'], ))
                con.commit()
            else:
                cur.execute('update users set user_mail = ?, user_sign = ?, user_logo = ?, user_perm = ?, user_utms = ? where user_id = ?',\
                        (user_mail, user_sign, user_logo, user_perm, self.stime(), user['user_id'], ))
                con.commit()
            if cur.rowcount:
                self.model('alogs').add(self.dbase('alogs'), "更新用户：" + str(user['user_id']), alog_data = user['user_name'], user_ip = self.request.remote_ip, user_id = self.current_user['user_id'], user_name = self.current_user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_UserCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/user-create.html')

    @admin
    def post(self):
        user = self.current_user

        try:
            user_name = self.input('user_name')
            user_mail = self.input('user_mail')
            user_perm = self.input('user_perm')
            user_pswd = self.input('user_pswd')
            user_rpwd = self.input('user_rpwd')
            user_sign = self.input('user_sign', '')
            user_logo = self.input('user_logo', '')
            user_ctms = self.stime()
            user_utms = user_ctms
            user_atms = user_ctms

            if len(user_name) < 1:
                self.flash(0, {'msg': '无效的用户帐号'})
                return
            
            if len(user_pswd) < 6 or (user_pswd != user_rpwd):
                self.flash(0, {'msg': '无效的用户密码'})
                return

            user_auid = self.model('admin').generate_randauid()
            user_salt = self.model('admin').generate_randsalt()
            user_pswd = self.model('admin').generate_password(user_rpwd, user_salt)
            user_perm = int(user_perm) & 0x7FFFFFFF

            con = self.dbase('users')
            cur = con.cursor()
            cur.execute('insert into users (\
                    user_auid, user_name, user_salt, user_pswd, user_perm, \
                    user_mail, user_sign, user_logo, user_ctms, user_utms, user_atms) \
                    values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                    (user_auid, user_name, user_salt, user_pswd, user_perm, \
                    user_mail, user_sign, user_logo, user_ctms, user_utms, user_atms))
            con.commit()
            cur.close()
            if cur.lastrowid:
                self.model('alogs').add(self.dbase('alogs'), "新增用户：" + str(cur.lastrowid), alog_data = user_name, user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
