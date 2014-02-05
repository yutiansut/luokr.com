#coding=utf-8

from admin import alive, AdminCtrl

class Admin_IndexCtrl(AdminCtrl):
    @alive
    def get(self, *args):
        cur = self.dbase('remas').cursor()
        cur.execute('select * from remas order by rema_id desc limit 3')
        remas = cur.fetchall()
        cur.close()

        cur = self.dbase('mails').cursor()
        cur.execute('select * from mails order by mail_id desc limit 3')
        mails = cur.fetchall()
        cur.close()

        self.render('admin/index.html', remas = remas, mails = mails)
