#coding=utf-8

class PostsModel:
    @staticmethod
    def get_by_pid(datum, pid):
        return datum.single('select * from posts where post_id = ?', (pid, ))
