#coding=utf-8

from basic import BasicCtrl

class ErrorCtrl(BasicCtrl):
    def get(self, *args):
        return self.send_error(404)
    def post(self, *args):
        return self.send_error(404)
