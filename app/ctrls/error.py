# -*- coding: UTF-8 -*-

from app.ctrls.basic import BasicCtrl

class ErrorCtrl(BasicCtrl):
    def get(self, *args):
        self.send_error(404)

    def post(self, *args):
        self.send_error(404)
