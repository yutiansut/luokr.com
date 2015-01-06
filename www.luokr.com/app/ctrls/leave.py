#coding=utf-8

from basic import alive, BasicCtrl

class LeaveCtrl(BasicCtrl):
    @alive
    def get(self):
        self.render('leave.html')

    @alive
    def post(self):
        self.del_current_sess()
        self.redirect('/')
