#coding=utf-8
import time

class ConfsModel:
    _map = {}

    @staticmethod
    def rst(dbase):
        ConfsModel._map = {}

    @staticmethod
    def get(dbase, name):
        if name in ConfsModel._map:
            return ConfsModel._map[name]

        cur = dbase.cursor()
        cur.execute('select conf_vals from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()

        if ret:
            ConfsModel._map[name] = ret['conf_vals']
        else:
            ConfsModel._map[name] = None

        return ConfsModel._map[name]

    @staticmethod
    def has(dbase, name):
        cur = dbase.cursor()
        cur.execute('select 1 from confs where conf_name = ?', (name, ))
        ret = cur.fetchone()
        cur.close()

        return bool(ret)

    @staticmethod
    def set(dbase, name, vals):
        cur = dbase.cursor()
        cur.execute('replace into confs (conf_name, conf_vals, conf_ctms) values (?, ?, ?)', (name, vals, int(time.time()),))
        dbase.commit()
        cur.close()

        ConfsModel._map[name] = vals

    @staticmethod
    def delete(dbase, name):
        cur = dbase.cursor()
        cur.execute('delete from confs where conf_name = ?', (name, ))
        dbase.commit()
        cur.close()

        ConfsModel._map[name] = None
