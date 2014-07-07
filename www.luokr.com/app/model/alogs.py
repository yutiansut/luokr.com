#coding=utf-8
import time

class AlogsModel:
    @staticmethod
    def add(dbase, alog_text, alog_data = '', user_ip = '', user_id = 0, user_name = ''):
        cur = dbase.cursor()
        cur.execute('insert into alogs (user_ip, user_id, user_name, alog_text, alog_data, alog_ctms) values (?, ?, ?, ?, ?, ?)',\
                (user_ip, user_id, user_name, alog_text, alog_data, int(time.time())))
        dbase.commit()
        cur.close()
        return cur.lastrowid
