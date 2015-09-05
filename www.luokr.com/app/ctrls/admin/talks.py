#coding=utf-8

from admin import admin, AdminCtrl

class Admin_TalksCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(max(int(self.input('qnty', 10)), 1), 100)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['lgth'] = 0;

        cur = self.dbase('talks').cursor()
        cur.execute('select * from talks order by talk_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        talks = cur.fetchall()
        cur.close()

        if talks:
            pager['lgth'] = len(talks)

        self.render('admin/talks.html', pager = pager, talks = talks)

class Admin_TalkCtrl(AdminCtrl):
    @admin
    def get(self):
        talk_id = self.input('talk_id')

        cur = self.dbase('talks').cursor()
        cur.execute('select * from talks where talk_id = ?', (talk_id ,))
        talk = cur.fetchone()
        cur.close()

        self.render('admin/talk.html', talk = talk)

    @admin
    def post(self):
        try:
            talk_id   = self.input('talk_id')
            talk_rank = self.input('talk_rank')
            talk_text = self.input('talk_text')
            talk_utms = self.stime()

            con = self.dbase('talks')
            cur = con.cursor()
            cur.execute('update talks set talk_rank = ?, talk_text = ?, talk_utms = ? where talk_id = ?', \
                    (talk_rank, talk_text, talk_utms, talk_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.ualog(self.current_user, '更新评论：' + str(talk_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_TalkHiddenCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            talk_id = self.input('talk_id')

            con = self.dbase('talks')
            cur = con.cursor()
            cur.execute('update talks set talk_rank=0 where talk_id = ?', (talk_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_TalkDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            talk_id   = self.input('talk_id')
            talk_ctms = self.input('talk_ctms')

            con = self.dbase('talks')
            cur = con.cursor()
            cur.execute('delete from talks where talk_id = ? and talk_ctms = ?', (talk_id, talk_ctms ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.ualog(self.current_user, '删除评论：' + str(talk_id))
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
