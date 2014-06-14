#coding=utf-8

from basic import BasicCtrl

class LeaveCtrl(BasicCtrl):
    def get(self):
        if self.current_user:
            self.render('leave.html')
            return
        self.redirect('/')

    def post(self):
        if self.current_user:
            self.del_current_user()
            self.redirect('/')
            return
        self.flash(0)
