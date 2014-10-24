#coding=utf-8

from basic import BasicCtrl

class ScoreCtrl(BasicCtrl):
    def post(self):
        pid = self.input('p', None)
        if not pid:
            self.flash(0)
            return

        con_posts = self.dbase('posts')
        cur_posts = con_posts.cursor()

        cur_posts.execute('update posts set post_rank = post_rank + 1, post_plus = post_plus + 1 where post_id = ? limit 1', (pid,))

        con_posts.commit()
        cur_posts.close()

        self.flash(1)
