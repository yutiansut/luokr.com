#coding=utf-8

import time
import re

class Cache:
    _s = {}

    @staticmethod
    def get(key):
        if (key in Cache._s) and ('val' in Cache._s[key]) and ('lvt' in Cache._s[key]) and (Cache._s[key]['lvt'] > int(time.time())):
            return Cache._s[key]['val']

    @staticmethod
    def set(key, val, lft = 3600):
        Cache._s[key] = {'val': val, 'lvt': int(time.time()) + int(lft)}

    @staticmethod
    def delete(key, exp = False):
        if exp:
            for k in Cache._s:
                if re.search(key, k):
                    Cache._s[k] = {'val': None, 'lvt': 0}
        elif (key in Cache._s):
            Cache._s[key] = {'val': None, 'lvt': 0}
