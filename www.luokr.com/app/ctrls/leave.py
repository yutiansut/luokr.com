#coding=utf-8

from basic import logon, BasicCtrl

class LeaveCtrl(BasicCtrl):
    @logon
    def get(self):
        self.render('leave.html')

    @logon
    def post(self):
        self.del_current_sess()
        self.redirect('/')
