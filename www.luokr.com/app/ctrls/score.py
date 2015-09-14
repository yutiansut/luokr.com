#coding=utf-8

from basic import BasicCtrl

class ScoreCtrl(BasicCtrl):
    def post(self):
        pid = self.input('p', None)
        if not pid:
            self.flash(0)
            return

        try:
            self.datum('posts').affect(
                    'update posts set post_rank = post_rank + 1, post_plus = post_plus + 1 where post_id = ? limit 1', (pid,))
            self.flash(1)
        except:
            self.flash(0)
