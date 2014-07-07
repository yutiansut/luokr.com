#coding=utf-8

import hashlib

class Utils:
    @staticmethod
    def array_keyto(ary, key):
        ret = {}
        for val in ary:
            ret[val[key]] = val
        return ret

    @staticmethod
    def array_group(ary, key):
        ret = {}
        for val in ary:
            if val[key] not in ret:
                ret[val[key]] = []
            ret[val[key]].append(val)
        return ret

    @staticmethod
    def array_field(ary, key):
        ret = []
        for val in ary:
            ret.append(val[key])
        return ret

    @staticmethod
    def str_md5(val):
        return hashlib.md5(val).hexdigest()
