#coding=utf-8

class PostsModel:
    @staticmethod
    def get_by_pid(dbase, pid):
        cur = dbase.cursor()
        cur.execute('select * from posts where post_id = ?', (pid, ))
        ret = cur.fetchone()
        cur.close()
        return ret
