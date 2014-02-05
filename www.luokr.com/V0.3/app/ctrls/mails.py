#coding=utf-8

from basic import BasicCtrl

class MailCtrl(BasicCtrl):
    def post(self):
        if not self.human_valid():
            self.flash(0)
            return

        name = self.input('name')
        mail = self.input('mail')
        text = self.input('text')
        time = self.stime()

        con = self.dbase('mails')

        cur = con.cursor()
        cur.execute('insert into mails (user_ip, user_name, user_mail, mail_text, mail_ctms, mail_utms) values (?, ?, ?, ?, ?, ?)', \
                (self.request.remote_ip, name, mail, text, time, time))
        con.commit()
        cur.close()

        if (cur.lastrowid):
            self.flash(1)
        else:
            self.flash(0)
