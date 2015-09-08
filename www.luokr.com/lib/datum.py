#coding=utf-8

class Datum:
    def __init__(self, source):
        # Sqlite3 Object
        self.source = source

    def cursor(self, *args, **kwargs):
        return self.source.cursor(*args, **kwargs)

    def commit(self, *args, **kwargs):
        return self.source.commit(*args, **kwargs)

    def revert(self, *args, **kwargs):
        return self.source.rollback(*args, **kwargs)

    def result(self, *args, **kwargs):
        cur = self.source.cursor()
        cur.execute(*args, **kwargs)
        ret = cur.fetchall()
        cur.close()
        return ret

    def single(self, *args, **kwargs):
        cur = self.source.cursor()
        cur.execute(*args, **kwargs)
        ret = cur.fetchone()
        cur.close()
        return ret

    def invoke(self, *args, **kwargs):
        return self.source.execute(*args, **kwargs)

    def affect(self, *args, **kwargs):
        con = self.source
        cur = con.execute(*args, **kwargs)
        con.commit()
        return cur
