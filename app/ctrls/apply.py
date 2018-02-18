# -*- coding: UTF-8 -*-

from app.ctrls.basic import BasicCtrl

class ApplyCtrl(BasicCtrl):
    def get(self):
        self.redirect("/about#email")
