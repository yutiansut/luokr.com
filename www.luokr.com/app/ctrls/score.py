#coding=utf-8

from basic import BasicCtrl

class ScoreCtrl(BasicCtrl):
    def post(self):
        post = self.model('posts').get_by_pid(self.dbase('posts'), self.input('p'))
        if not post:
            self.flash(0, {'msg': '文章不存在'})
            return

        con_posts = self.dbase('posts')
        cur_posts = con_posts.cursor()

        cur_posts.execute('update posts set post_rank = post_rank + 1, post_plus = post_plus + 1 where post_id = ?', (post['post_id'],))

        con_posts.commit()
        cur_posts.close()

        self.flash(1)
