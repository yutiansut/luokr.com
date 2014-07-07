#coding=utf-8

from basic import BasicCtrl

class LinksCtrl(BasicCtrl):
    def get(self):
        cur = self.dbase('links').cursor()
        cur.execute('select * from links where link_rank>0 order by link_rank desc, link_id desc')
        links = cur.fetchall()
        cur.close()

        self.render('links.html', links = links)
