#coding=utf-8
import time

class PostsModel:
    @staticmethod
    def get_by_pid(dbase, post_id):
        cur = dbase.cursor()
        cur.execute('select * from posts where post_id = ?', (post_id, ))
        post = cur.fetchone()
        cur.close()
        return post
