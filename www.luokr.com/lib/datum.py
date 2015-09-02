#coding=utf-8

class Datum:
    def __init__(self, dbase):
        self.source = dbase

    def getall(self, tbnm, cond, args = [], find = '*'):
        if cond != '':
            cond = ' WHERE ' + cond

        cur = self.source.cursor()
        cur.execute('SELECT %s FROM %s%s' % (find, tbnm, cond), tuple(args))
        ret = cur.fetchall()
        cur.close()
        return ret

    def getone(self, tbnm, cond, args = [], find = '*'):
        if cond != '':
            cond = ' WHERE ' + cond

        cur = self.source.cursor()
        cur.execute('SELECT %s FROM %s%s' % (find, tbnm, cond), tuple(args))
        ret = cur.fetchone()
        cur.close()
        return ret

    def insert(self, tbnm, maps):
        ques = []
        keys = []
        vals = []
        for k in maps:
            ques.append('?')
            keys.append(k)
            vals.append(maps[k])

        con = self.source
        cur = con.cursor()
        cur.execute('INSERT INTO %s (%s) VALUES (%s)' % (tbnm, ','.join(keys), ','.join(ques)), tuple(vals))
        con.commit()
        cur.close()
        return cur.lastrowid

    def update(self, tbnm, maps, cond, args = []):
        ques = []
        vals = []
        for k in maps:
            ques.append(k + '=?')
            vals.append(maps[k])
        vals.extend(args)

        if cond != '':
            cond = ' WHERE ' + cond

        con = self.source
        cur = con.cursor()
        cur.execute('UPDATE %s SET %s%s' % (tbnm, ','.join(ques), cond), tuple(vals))
        con.commit()
        cur.close()
        return cur.rowcount

    def delete(self, tbnm, cond, args = []):
        if cond != '':
            cond = ' WHERE ' + cond

        con = self.source
        cur = con.cursor()
        cur.execute('DELETE FROM %s%s' % (tbnm, cond), tuple(args))
        con.commit()
        cur.close()
        return cur.rowcount
