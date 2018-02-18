# -*- coding: UTF-8 -*-

from app.ctrls.basic import BasicCtrl

class HelloCtrl(BasicCtrl):
    def get(self):
        self.write('Hello\n' + self.timer().strftime('%F %T %Z'))
