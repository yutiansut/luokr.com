#coding=utf-8

from admin import admin, AdminCtrl

class Admin_IndexCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        cur = self.dbase('talks').cursor()
        cur.execute('select * from talks order by talk_id desc limit 3')
        talks = cur.fetchall()
        cur.close()

        cur = self.dbase('mails').cursor()
        cur.execute('select * from mails order by mail_id desc limit 3')
        mails = cur.fetchall()
        cur.close()

        self.render('admin/index.html', talks = talks, mails = mails)
