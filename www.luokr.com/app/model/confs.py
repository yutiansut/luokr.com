#coding=utf-8
import time

class ConfsModel:
    def __init__(self):
        self.reload()

    def reload(self, dbase = None):
        self._cache = {}
        if dbase is not None:
            cur = dbase.cursor()
            cur.execute('select conf_name, conf_vals from confs')
            ret = cur.fetchall()
            cur.close()
            if ret:
                for row in ret:
                    self._cache[row['conf_name']] = row['conf_vals']

    def obtain(self, dbase, name):
        if name in self._cache:
            return self._cache[name]
        cur = dbase.cursor()
        cur.execute('select conf_vals from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()
        if ret:
            self._cache[name] = ret['conf_vals']
        else:
            self._cache[name] = None
        return self._cache[name]

    def exists(self, dbase, name):
        cur = dbase.cursor()
        cur.execute('select 1 from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()
        return bool(ret)

    def upsert(self, dbase, name, vals):
        cur = dbase.cursor()
        cur.execute('replace into confs (conf_name, conf_vals, conf_ctms) values (?, ?, ?)', (name, vals, int(time.time()),))
        dbase.commit()
        cur.close()
        self._cache[name] = vals

    def delete(self, dbase, name):
        cur = dbase.cursor()
        cur.execute('delete from confs where conf_name = ?', (name, ))
        dbase.commit()
        cur.close()
        self._cache[name] = None
