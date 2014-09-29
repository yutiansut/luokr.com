#coding=utf-8

from admin import admin, AdminCtrl

class Admin_MailsCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('mails').cursor()
        cur.execute('select * from mails order by mail_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        mails = cur.fetchall()
        cur.close()

        if mails:
            pager['list'] = len(mails)

        self.render('admin/mails.html', pager = pager, mails = mails)

class Admin_MailAccessCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            mail_id = self.input('mail_id')

            con = self.dbase('mails')
            cur = con.cursor()
            cur.execute('update mails set mail_stat=1, mail_utms=? where mail_id = ?', (self.stime(), mail_id,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_MailDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            user = self.current_user

            mail_id   = self.input('mail_id')
            mail_utms = self.input('mail_utms')

            con = self.dbase('mails')
            cur = con.cursor()
            cur.execute('delete from mails where mail_id = ? and mail_utms = ?', (mail_id, mail_utms ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.model('alogs').add(self.dbase('alogs'), '删除留言：' + str(mail_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
