#coding=utf-8

from admin import alive, AdminCtrl

class Admin_UsersCtrl(AdminCtrl):
    @alive
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('users').cursor()
        cur.execute('select * from users order by user_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        users = cur.fetchall()
        cur.close()

        if users:
            pager['list'] = len(users)

        self.render('admin/users.html', users = users, pager = pager)
