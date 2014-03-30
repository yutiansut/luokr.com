#coding=utf-8

from admin import alive, AdminCtrl

class Admin_MailsCtrl(AdminCtrl):
    @alive
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
    @alive
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
