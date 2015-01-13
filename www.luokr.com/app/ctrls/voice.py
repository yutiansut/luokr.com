#coding=utf-8

from basic import BasicCtrl

class VoiceCtrl(BasicCtrl):
    def post(self):
        if not self.human_valid():
            self.flash(0, {'msg': '验证码错误'})
            return

        post = self.model('posts').get_by_pid(self.dbase('posts'), self.input('p'))
        if not post:
            self.flash(0, {'msg': '文章不存在'})
            return

        rank = '0'
        usid = '0'
        if self.input('auth', False) and self.current_user:
            rank = self.get_runtime_conf('posts_talks_min_rank')
            usid = self.current_user['user_id']
            name = self.current_user['user_name']
            mail = self.current_user['user_mail']
        else:
            name = self.input('name')
            mail = self.input('mail')

        text = self.input('text')
        time = self.stime()

        con_talks = self.dbase('talks')
        cur_talks = con_talks.cursor()
        cur_talks.execute('insert into talks (post_id, user_ip, user_id, user_name, user_mail, talk_text, talk_rank, talk_ctms, talk_utms) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                (post['post_id'], self.request.remote_ip, usid, name, mail, text, rank, time, time))
        con_talks.commit()
        cur_talks.close()

        if cur_talks.lastrowid:
            con_posts = self.dbase('posts')
            cur_posts = con_posts.cursor()
            cur_posts.execute('update posts set post_refc = post_refc + 1 where post_id = ?', (post['post_id'],))
            con_posts.commit()
            cur_posts.close()

            if float(rank) > 0:
                self.flash(1, {'msg': '评论发表成功'})
            else:
                self.flash(1, {'msg': '当前评论内容暂不公开'})
            return
        self.flash(0)
