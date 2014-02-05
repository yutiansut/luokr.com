#coding=utf-8

from basic import BasicCtrl

class PostsCtrl(BasicCtrl):
    def get(self, _tnm = None):
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        track = ''

        cur = self.dbase('posts').cursor()

        stime = self.stime()

        _tid = 0
        if _tnm:
            cur.execute('select term_id from terms where term_sign = ? limit 1', (str(_tnm).lower(), ))
            _tid = cur.fetchone()
            if _tid:
                _tid = _tid['term_id']

        _top = False
        _kws = self.input('k', None)

        if _tid:
            cur.execute('select posts.* from posts,post_terms where posts.post_id=post_terms.post_id and term_id=? and post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?', (_tid, stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur.fetchall()
            track = '标签：' + _tnm
        elif _tnm:
            self.send_error(404)
            return
        elif _kws:
            cur.execute('select * from posts where post_stat>0 and post_ptms<? and post_content like ? order by post_ptms desc limit ? offset ?', (stime, '%'+_kws+'%', pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur.fetchall()
            track = '搜索：' + _kws
        else:
            cur.execute('select * from posts where post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?', (stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur.fetchall()

            if self.input('page', None) is None:
                _top = True

        ptids = {}
        ptags = {}
        if posts:
            pager['list'] = len(posts)

            cur.execute('select post_id,term_id from post_terms where post_id in (' + ','.join(str(i['post_id']) for i in posts) + ')')
            ptids = cur.fetchall()
            if ptids:
                cur.execute('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
                ptags = cur.fetchall()
                if ptags:
                    ptids = self.utils().array_group(ptids, 'post_id')
                    ptags = self.utils().array_keyto(ptags, 'term_id')

        keyws_tag = self.cache().get('posts:keyws_tag')
        if not keyws_tag:
            cur.execute('select * from terms where term_refc>0 order by term_refc desc, term_id desc limit 32')
            keyws_tag = cur.fetchall()
            self.cache().set('posts:keyws_tag', keyws_tag)

        posts_top = self.cache().get('posts:posts_top')
        if not posts_top:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_rank desc, post_id desc limit 9', (stime,))
            posts_top = cur.fetchall()
            self.cache().set('posts:posts_top', posts_top)

        posts_hot = self.cache().get('posts:posts_hot')
        if not posts_hot:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_remc desc, post_id desc limit 9', (stime,))
            posts_hot = cur.fetchall()
            self.cache().set('posts:posts_hot', posts_hot)

        posts_new = self.cache().get('posts:posts_new')
        if not posts_new:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_ptms desc, post_id desc limit 9', (stime,))
            posts_new = cur.fetchall()
            self.cache().set('posts:posts_new', posts_new)

        cur.close()

        remas_new = self.cache().get('posts:remas_new')
        if not remas_new:
            cur = self.dbase('remas').cursor()
            cur.execute('select * from remas where rema_rank>0 order by rema_id desc limit 9')
            remas_new = cur.fetchall()
            cur.close()
            self.cache().set('posts:remas_new', remas_new)

        if _top:
            links_top = self.cache().get('posts:links_top')
            if not links_top:
                cur = self.dbase('links').cursor()
                cur.execute('select * from links where link_rank>0 order by link_rank desc limit 9')
                links_top = cur.fetchall()
                cur.close()
                self.cache().set('posts:links_top', links_top)
        else:
            links_top = None

        self.render('posts.html', track = track, pager = pager, posts = posts, ptids = ptids, ptags = ptags\
                , posts_top = posts_top, posts_hot = posts_hot, posts_new = posts_new, keyws_tag = keyws_tag, remas_new = remas_new, links_top = links_top)


class PostCtrl(BasicCtrl):
    def get(self, post_id):
        stime = self.stime()

        cur = self.dbase('posts').cursor()
        cur.execute('select * from posts where post_id = ?', (post_id, ))
        post = cur.fetchone()

        if not post or ((not self.get_current_user()) and (not post['post_stat'] or post['post_ptms'] >= stime)):
            cur.close()
            return self.send_error(404)

        ptids = {}
        ptags = {}
        if post:
            cur.execute('select post_id,term_id from post_terms where post_id = ?', (post_id, ))
            ptids = cur.fetchall()
            if ptids:
                cur.execute('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
                ptags = cur.fetchall()
                if ptags:
                    ptids = self.utils().array_group(ptids, 'post_id')
                    ptags = self.utils().array_keyto(ptags, 'term_id')

        cur.execute('select post_id from posts where post_stat>0 and post_ptms<? and post_id<? order by post_id desc limit 1', (stime, post_id, ))
        post_prev = cur.fetchone()
        if post_prev:
            post_prev = post_prev['post_id']
        else:
            post_prev = 0

        cur.execute('select post_id from posts where post_stat>0 and post_ptms<? and post_id>? order by post_id asc limit 1', (stime, post_id, ))
        post_next = cur.fetchone()
        if post_next:
            post_next = post_next['post_id']
        else:
            post_next = 0

        keyws_tag = self.cache().get('posts:keyws_tag')
        if not keyws_tag:
            cur.execute('select * from terms where term_refc>0 order by term_refc desc, term_id desc limit 32')
            keyws_tag = cur.fetchall()
            self.cache().set('posts:keyws_tag', keyws_tag)

        posts_top = self.cache().get('posts:posts_top')
        if not posts_top:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_rank desc, post_id desc limit 9', (stime,))
            posts_top = cur.fetchall()
            self.cache().set('posts:posts_top', posts_top)

        posts_hot = self.cache().get('posts:posts_hot')
        if not posts_hot:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_remc desc, post_id desc limit 9', (stime,))
            posts_hot = cur.fetchall()
            self.cache().set('posts:posts_hot', posts_hot)

        posts_new = self.cache().get('posts:posts_new')
        if not posts_new:
            cur.execute('select post_id,post_title,post_ptms from posts where post_stat>0 and post_ptms<? order by post_ptms desc, post_id desc limit 9', (stime,))
            posts_new = cur.fetchall()
            self.cache().set('posts:posts_new', posts_new)

        cur.close()

        cur = self.dbase('remas').cursor()

        remas_new = self.cache().get('posts:remas_new')
        if not remas_new:
            cur.execute('select * from remas where rema_rank>0 order by rema_id desc limit 9')
            remas_new = cur.fetchall()
            self.cache().set('posts:remas_new', remas_new)

        cur.execute('select * from remas where post_id = ? and rema_rank > 0 order by rema_id desc', (post['post_id'],))
        remas = cur.fetchall()
        cur.close()

        links_top = None

        self.render('post.html', post = post, ptids = ptids, ptags = ptags, remas = remas\
                , post_prev = post_prev, post_next = post_next\
                , posts_top = posts_top, posts_hot = posts_hot, posts_new = posts_new, keyws_tag = keyws_tag, remas_new = remas_new, links_top = links_top)
