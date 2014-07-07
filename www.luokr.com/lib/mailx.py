#coding=utf-8
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Header import Header

class Mailx:
    def __init__(self, conf):
        self.conf = conf

    def send(self, to_list, subject, content, subtype='plain', charset='UTF-8', attachs=[]):
        if 'smtp_able' not in self.conf or not self.conf['smtp_able']:
            return False

        if not to_list:
            return False

        msgs = MIMEMultipart('alternative')
        msgs['Subject'] = Header(subject, charset)
        msgs['From'] = self.conf['smtp_from']
        msgs['To'] = ';'.join(to_list)

        msgs.attach(MIMEText(content, _subtype=subtype, _charset=charset))
        for item in attachs:
            msgs.attach(item)

        try:
            smtp = smtplib.SMTP(self.conf['smtp_host'], self.conf['smtp_port'])
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            smtp.login(self.conf['smtp_user'], self.conf['smtp_pswd'])
            smtp.sendmail(self.conf['smtp_from'], to_list, msgs.as_string())
            smtp.quit()

            return True
        except Exception, e:
            print str(e)
            return False
