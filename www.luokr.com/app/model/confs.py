#coding=utf-8
import time

class ConfsModel:
    def __init__(self):
        self.rst()

    def rst(self):
        self._s = {}

    def get(self, dbase, name):
        if name in self._s:
            return self._s[name]

        cur = dbase.cursor()
        cur.execute('select conf_vals from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()

        if ret:
            self._s[name] = ret['conf_vals']
        else:
            self._s[name] = None

        return self._s[name]

    def has(self, dbase, name):
        cur = dbase.cursor()
        cur.execute('select 1 from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()

        return bool(ret)

    def set(self, dbase, name, vals):
        cur = dbase.cursor()
        cur.execute('replace into confs (conf_name, conf_vals, conf_ctms) values (?, ?, ?)', (name, vals, int(time.time()),))
        dbase.commit()
        cur.close()

        self._s[name] = vals

    def delete(self, dbase, name):
        cur = dbase.cursor()
        cur.execute('delete from confs where conf_name = ?', (name, ))
        dbase.commit()
        cur.close()

        self._s[name] = None
