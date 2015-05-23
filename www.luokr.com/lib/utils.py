#coding=utf-8

import re
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
    def build_links(val, opt = ' target="_blank"'):
        exp = re.compile(
                r'((?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/[?&=A-Z0-9-]*)?)', re.IGNORECASE)
        return exp.sub(r'<a href="\1"' + opt + r'>\1</a>', val)

    @staticmethod
    def str_md5(val):
        return hashlib.md5(val).hexdigest()
