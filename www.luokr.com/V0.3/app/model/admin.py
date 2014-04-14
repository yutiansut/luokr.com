#coding=utf-8

import random, hashlib

class AdminModel:
    @staticmethod
    def generate_randsalt(list = '0123456789abcdefghijklmnopqrstuvwxyz', size = 8):
        return ''.join(random.sample(list, size))

    @staticmethod
    def generate_password(pswd, salt):
        return hashlib.md5('AL.pswd:' + hashlib.md5(str(pswd) + '#'  + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def generate_authword(atms, salt):
        return hashlib.md5('AL.auth:' + hashlib.md5(str(atms) + '!'  + str(salt)).hexdigest()).hexdigest()

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

    @staticmethod
    def chk_user_is_root(user):
        if type(user) == type({}) and 'role' in user and user['role'] == 0x7FFFFFFF:
            return True
        else:
            return False
