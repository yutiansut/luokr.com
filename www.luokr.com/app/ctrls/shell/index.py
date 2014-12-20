#coding=utf-8

from shell import shell, ShellCtrl

class Shell_IndexCtrl(ShellCtrl):
    def get(self, name):
        stime = self.stime()
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        user = self.model('admin').get_user_by_name(self.dbase('users'), name)
        if not user:
            self.flash(0, {'sta': 404})
            return

        cur_posts = self.dbase('posts').cursor()
        cur_posts.execute('select * from posts where user_id=? and post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?', (user['user_id'], stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        posts = cur_posts.fetchall()

        if posts:
            pager['list'] = len(posts)

        if self.input('_pjax', None) == '#shell-index-posts':
            self.render('shell/index/posts.html', user = user, pager = pager, posts = posts)
            return

        self.render('shell/index.html', user = user, pager = pager, posts = posts)
