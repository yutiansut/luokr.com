#coding=utf-8

import hashlib

class AdminModel:
    @staticmethod
    def generate_password(pswd, salt):
        return hashlib.md5('AL.pswd:' + hashlib.md5(pswd + '#'  + salt).hexdigest()).hexdigest()

    @staticmethod
    def get_user_by_usid(dbase, usid):
        cur = dbase.cursor()
        cur.execute('select * from users where user_id = ?', (usid,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def get_user_by_sign(dbase, sign):
        cur = dbase.cursor()
        cur.execute('select * from users where user_sign = ?', (sign,))
        user = cur.fetchone()
        cur.close()
        return user
