#coding=utf-8

from basic import BasicCtrl

class ErrorCtrl(BasicCtrl):
    def get(self, *args):
        self.flash(0, {'sta': 404})

    def post(self, *args):
        self.flash(0, {'sta': 404})
