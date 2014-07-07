#coding=utf-8

from admin import admin, AdminCtrl

class Admin_LinksCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('links').cursor()
        cur.execute('select * from links order by link_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        links = cur.fetchall()
        cur.close()

        if links: 
            pager['list'] = len(links)

        self.render('admin/links.html', pager = pager, links = links)

class Admin_LinkCtrl(AdminCtrl):
    @admin
    def get(self):
        link_id = self.input('link_id')
        cur = self.dbase('links').cursor()
        cur.execute('select * from links where link_id = ?', (link_id,))
        link = cur.fetchone()

        self.render('admin/link.html', entry = link)

    @admin
    def post(self):
        try:
            user = self.current_user

            link_id   = self.input('link_id')
            link_name = self.input('link_name')
            link_href = self.input('link_href')
            link_desp = self.input('link_desp')
            link_rank = self.input('link_rank')
            link_utms = self.stime()

            con = self.dbase('links')
            cur = con.cursor()
            cur.execute('update links set link_name = ?, link_href = ?, link_desp = ?, link_rank = ?, link_utms = ? where link_id = ?', \
                    (link_name, link_href, link_desp, link_rank, link_utms, link_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.model('alogs').add(self.dbase('alogs'), '更新链接：' + str(link_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_LinkCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/link-create.html')

    @admin
    def post(self):
        try:
            user = self.current_user

            link_name = self.input('link_name')
            link_href = self.input('link_href')
            link_desp = self.input('link_desp')
            link_rank = self.input('link_rank')
            link_ctms = self.stime()
            link_utms = link_ctms

            con = self.dbase('links')
            cur = con.cursor()
            cur.execute('insert into links (link_name, link_href, link_desp, link_rank, link_ctms, link_utms) values (?, ?, ?, ?, ?, ?)', \
                    (link_name, link_href, link_desp, link_rank, link_ctms, link_utms ,))
            con.commit()
            cur.close()
            if cur.lastrowid:
                self.model('alogs').add(self.dbase('alogs'), "新增链接：" + str(cur.lastrowid), alog_data = link_href, user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_LinkDeleteCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            user = self.current_user

            link_id   = self.input('link_id')
            link_utms = self.input('link_utms')

            con = self.dbase('links')
            cur = con.cursor()
            cur.execute('delete from links where link_id = ? and link_utms = ?', (link_id, link_utms ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.model('alogs').add(self.dbase('alogs'), '删除链接：' + str(link_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
