#coding=utf-8

from admin import admin, AdminCtrl

class Admin_TermsCtrl(AdminCtrl):
    @admin
    def get(self, *args):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur = self.dbase('terms').cursor()
        cur.execute('select * from terms order by term_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        terms = cur.fetchall()
        cur.close()

        if terms:
            pager['list'] = len(terms)

        self.render('admin/terms.html', terms = terms, pager = pager)

class Admin_TermCtrl(AdminCtrl):
    @admin
    def get(self):
        term_id = self.input('term_id')
        cur = self.dbase('terms').cursor()
        cur.execute('select * from terms where term_id = ?', (term_id,))
        term = cur.fetchone()

        self.render('admin/term.html', entry = term)

    @admin
    def post(self):
        try:
            term_id   = self.input('term_id')
            term_name = self.input('term_name')

            con = self.dbase('terms')
            cur = con.cursor()
            cur.execute('update terms set term_name = ? where term_id = ?', \
                    (term_name, term_id ,))
            con.commit()
            cur.close()
            if cur.rowcount:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)

class Admin_TermCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        self.render('admin/term-create.html')

    @admin
    def post(self):
        try:
            term_name = self.input('term_name')
            term_ctms = self.stime()

            con = self.dbase('terms')
            cur = con.cursor()
            cur.execute('insert into terms (term_name, term_ctms) values (?, ?)', \
                    (term_name, term_ctms ,))
            con.commit()
            cur.close()
            if cur.lastrowid:
                self.flash(1)
                return
        except:
            pass
        self.flash(0)
