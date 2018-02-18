# -*- coding: UTF-8 -*-

from app.ctrls.basic import BasicCtrl

class AboutCtrl(BasicCtrl):
    def get(self, *args):
        self.render('about.html')
