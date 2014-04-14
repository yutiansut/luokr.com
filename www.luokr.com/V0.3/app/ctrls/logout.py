#coding=utf-8

from basic import BasicCtrl

class LogoutCtrl(BasicCtrl):
    def get(self):
        if self.current_user:
            try:
                self.input(self.utils().str_md5(str(self.current_user['user_id']) + self.fetch_xsrfs()))
                self.del_current_user()
                self.redirect('/')
                return
            except:
                pass
        self.flash(0)

    def post(self):
        return self.get()
