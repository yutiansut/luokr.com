#coding=utf-8

from basic import BasicCtrl

class LogoutCtrl(BasicCtrl):
    def get(self):
        sess = self.get_current_user()
        if sess:
            try:
                self.input(self.utils().str_md5(sess['user_sign'] + str(sess['user_utms'])))
                self.del_current_user()
                self.redirect('/')
                return
            except:
                pass
        self.flash(0)

    def post(self):
        return self.get()
