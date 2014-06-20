#coding=utf-8

from basic import BasicCtrl
from lib.mailx import Mailx

class EmailCtrl(BasicCtrl):
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
            self.finish()

            conf = self.get_runtime_conf('mailx')
            if conf:
                Mailx(self.get_escaper().json_decode(conf)).send(self.get_escaper().json_decode(self.get_runtime_conf('admin_email')),
                        'Received Feedback (%s)' % self.timer().strftime('%F %T %Z', self.timer().localtime(time)),
                        'Mail From %s<%s>:\r\n\r\n%s' %(name, mail, text))
        else:
            self.flash(0)
