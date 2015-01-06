#coding=utf-8

from basic import BasicCtrl

class LoginCtrl(BasicCtrl):
    def get(self):
        next = self.input('next', '/shell')
        self.render('login.html', next = next)

    def post(self):
        if not self.human_valid():
            self.flash(0, {'msg': '验证码错误'})
            return

        try:
            username = self.input('username')
            password = self.input('password')
            remember = self.input('remember', None)
            redirect = self.input('redirect', '/shell')

            if remember:
                remember = int(remember)

            user = self.model('admin').get_user_by_name(self.dbase('users'), username)

            if user:
                ckey = 'login:user#' + str(user['user_id'])
                cval = self.cache().get(ckey)
                self.cache().set(ckey, 1, 3)
                if cval:
                    self.flash(0, {'msg': '操作太频繁，请稍后再试'})
                    return

            if user and self.model('admin').generate_password(password, user['user_salt']) == user['user_pswd']:
                try:
                    usid = str(user['user_id'])
                    self.set_cookie("_usid", usid, expires_days=remember)

                    auid = str(user['user_auid'])
                    self.set_secure_cookie("_auid", auid, expires_days=remember, httponly = True)

                    auth = self.model('admin').generate_authword(user['user_atms'], user['user_salt'])
                    self.set_secure_cookie("_auth", auth, expires_days=remember, httponly = True)

                    self.flash(1, {'url': redirect})
                    self.model('alogs').add(self.dbase('alogs'), '登录', user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                except:
                    self.flash(0, {'msg': '请稍后再试'})
                return
        except:
            pass

        self.flash(0, {'msg': '用户名或密码错误'})
