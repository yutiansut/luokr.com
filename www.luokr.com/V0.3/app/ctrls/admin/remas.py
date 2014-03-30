#coding=utf-8

from admin import alive, AdminCtrl

class Admin_RemasCtrl(AdminCtrl):
    @alive
    def get(self):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('remas').cursor()
        cur.execute('select * from remas order by rema_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        remas = cur.fetchall()
        cur.close()

        if remas:
            pager['list'] = len(remas)

        self.render('admin/remas.html', pager = pager, remas = remas)

class Admin_RemaCtrl(AdminCtrl):
    @alive
    def get(self):
        rema_id = self.input('rema_id')

        cur = self.dbase('remas').cursor()
        cur.execute('select * from remas where rema_id = ?', (rema_id ,))
        rema = cur.fetchone()
        cur.close()

        self.render('admin/rema.html', rema = rema)

    @alive
    def post(self):
        try:
            user = self.fetch_admin()

            rema_id   = self.input('rema_id')
            rema_rank = self.input('rema_rank')
            rema_cont = self.input('rema_cont')
            rema_utms = self.stime()

            con = self.dbase('remas')
            cur = con.cursor()
            cur.execute('update remas set rema_rank = ?, rema_cont = ?, rema_utms = ? where rema_id = ?', \
                    (rema_rank, rema_cont, rema_utms, rema_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.model('alogs').add(self.dbase('alogs'), '更新评论：' + str(rema_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_RemaHiddenCtrl(AdminCtrl):
    @alive
    def post(self):
        try:
            rema_id = self.input('rema_id')

            con = self.dbase('remas')
            cur = con.cursor()
            cur.execute('update remas set rema_rank=0 where rema_id = ?', (rema_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
