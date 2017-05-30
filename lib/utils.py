# -*- coding: UTF-8 -*-

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
                r'('
                r'(?:http|ftp)s?://'           # http:// or https://
                r'[a-z0-9-]+(?:\.[a-z0-9-]+)*' # domain or ip...
                r'(?::\d+)?'                   # optional port
                r'(?:/[^@"\'<>\s]*)?'           # optional segs
                r')', re.IGNORECASE)
        val = exp.sub(r'<a href="\1"' + opt + r'>\1</a>', val)

        exp = re.compile(
                r'('
                r'([-a-z0-9_.]+)'                 # user name
                r'@'                              # @
                r'([a-z0-9-]+(?:\.[a-z0-9-]+)*)'  # domain
                r')', re.IGNORECASE)

        val = exp.sub(r'<a href="javascript:;"' + opt + r' onclick="location.href=' + r"'mailto:\2'" + r"+String.fromCharCode(64)+'" + r"\3'" + r'">\2<script>document.write(String.fromCharCode(64))</script>\3</a>', val)

        return val

    @staticmethod
    def str_md5_hex(val):
        return hashlib.md5(val).hexdigest()
