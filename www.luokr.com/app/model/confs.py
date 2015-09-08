#coding=utf-8
import time

class ConfsModel:
    def __init__(self):
        self.reload()

    def reload(self, datum = None):
        self._cache = {}
        if datum is not None:
            ret = datum.result('select conf_name, conf_vals from confs')
            if ret:
                for row in ret:
                    self._cache[row['conf_name']] = row['conf_vals']

    def obtain(self, datum, name):
        if name in self._cache:
            return self._cache[name]

        ret = datum.single('select conf_vals from confs where conf_name = ?', (name, ))
        if ret:
            self._cache[name] = ret['conf_vals']
        else:
            self._cache[name] = None
        return self._cache[name]

    def exists(self, datum, name):
        ret = datum.single('select 1 from confs where conf_name = ?', (name, ))
        return bool(ret)

    def upsert(self, datum, name, vals):
        datum.affect('replace into confs (conf_name, conf_vals, conf_ctms) values (?, ?, ?)', (name, vals, int(time.time()),))
        self._cache[name] = vals

    def delete(self, datum, name):
        datum.affect('delete from confs where conf_name = ?', (name, ))
        self._cache[name] = None
