#coding=utf-8

import random, hashlib

class AdminModel:

    @staticmethod
    def generate_randauid(list = '-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', size = 64):
        auid = ''
        while (size > 0):
            auid = auid + random.choice(list)
            size = size - 1
        return auid

    @staticmethod
    def generate_randsalt(list = '0123456789abcdefghijklmnopqrstuvwxyz', size = 8):
        salt = ''
        while (size > 0):
            salt = salt + random.choice(list)
            size = size - 1
        return salt

    @staticmethod
    def generate_password(pswd, salt):
        return hashlib.md5('AL.pswd:' + hashlib.md5(str(pswd) + '#'  + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def generate_authword(atms, salt):
        return hashlib.md5('AL.auth:' + hashlib.md5(str(atms) + '$'  + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def get_user_by_usid(dbase, usid):
        cur = dbase.cursor()
        cur.execute('select * from users where user_id = ?', (usid,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def get_user_by_name(dbase, name):
        cur = dbase.cursor()
        cur.execute('select * from users where user_name = ?', (name,))
        user = cur.fetchone()
        cur.close()
        return user

    @staticmethod
    def chk_user_is_root(user):
        try:
            user = dict(user)
            return user and 'user_perm' in user and user['user_perm'] & 0x7FFFFFFF == 0x7FFFFFFF
        except:
            return False
