#coding=utf-8

from admin import admin, AdminCtrl

class Admin_AlogsCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('alogs').cursor()
        cur.execute('select * from alogs order by alog_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        alogs = cur.fetchall()
        cur.close()

        if alogs:
            pager['list'] = len(alogs)

        self.render('admin/alogs.html', alogs = alogs, pager = pager)
