#coding=utf-8

from basic import BasicCtrl

class LoginCtrl(BasicCtrl):
    def get(self):
        next = self.input('next', '/admin')
        if self.get_current_user():
            self.redirect(next)
            return

        self.render('login.html', next = next)

    def post(self):
        if not self.human_valid():
            self.flash(0, {'msg': '验证码错误'})
            return

        try:
            username = self.input('username')
            password = self.input('password')
            remember = self.input('remember', None)
            redirect = self.input('redirect', '/admin')

            if remember:
                remember = int(remember)

            user = self.model('admin').get_user_by_sign(self.dbase('users'), username)
            if user and self.model('admin').generate_password(password, user['user_salt']) == user['user_pswd']:
                try:
                    auth = self.model('admin').generate_authword(user['user_atms'], user['user_salt'])
                    self.set_secure_cookie("_auth", auth, expires_days=remember, httponly = True)
                    self.set_cookie("_usid", str(user['user_id']), expires_days=remember)

                    self.flash(1, {'url': redirect})
                    self.model('alogs').add(self.dbase('alogs'), '登录', user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                except:
                    self.flash(0, {'msg': '请稍后再试'})
                return
        except:
            pass

        self.flash(0, {'msg': '用户名或密码错误'})
