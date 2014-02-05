#coding=utf-8

from basic import BasicCtrl

class RemaCtrl(BasicCtrl):
    def post(self):
        try:
            if not self.human_valid():
                self.flash(0, {'msg': '验证码错误'})
                return

            post = self.model('posts').get_by_pid(self.dbase('posts'), self.input('p'))
            name = self.input('name')
            mail = self.input('mail')
            text = self.input('text')
            time = self.stime()

            con = self.dbase('posts')
            cur = con.cursor()
            cur.execute('update posts set post_remc = post_remc + 1 where post_id = ?', (post['post_id'],))
            con.commit()
            cur.close()

            con = self.dbase('remas')
            cur = con.cursor()
            cur.execute('insert into remas (post_id, user_ip, user_name, user_mail, rema_cont, rema_rank, rema_ctms, rema_utms) values (?, ?, ?, ?, ?, ?, ?, ?)', \
                    (post['post_id'], self.request.remote_ip, name, mail, text, 0, time, time))
            con.commit()
            cur.close()

            if (cur.lastrowid):
                self.flash(1, {'msg': '当前评论内容暂不公开'})
            else:
                self.flash(0)
        except:
            self.flash(0)
