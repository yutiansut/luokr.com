#coding=utf-8

from basic import BasicCtrl

class PostsCtrl(BasicCtrl):
    def get(self, _tnm = None):
        pager = {}
        pager['qnty'] = 5
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        stime = self.stime()
        track = ''

        cur_posts = self.dbase('posts').cursor()
        cur_terms = self.dbase('terms').cursor()
        cur_users = self.dbase('users').cursor()

        _qry = self.input('q', None)
        _top = False
        _tag = None

        if _tnm:
            cur_terms.execute('select * from terms where term_name = ? limit 1', (str(_tnm),))
            _tag = cur_terms.fetchone()

        if _tag:
            cur_posts.execute('select posts.* from posts,post_terms where posts.post_id=post_terms.post_id and term_id=? and post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?', (_tag['term_id'], stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur_posts.fetchall()
            track = '标签：' + _tag['term_name']
        elif _tnm:
            self.send_error(404)
            return
        elif _qry:
            cur_posts.execute('select * from posts where post_stat>0 and post_ptms<? and (post_title like ? or post_content like ?) order by post_ptms desc limit ? offset ?', (stime, '%'+_qry+'%', '%'+_qry+'%', pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur_posts.fetchall()
            track = '搜索：' + _qry
        else:
            cur_posts.execute('select * from posts where post_stat>0 and post_ptms<? order by post_ptms desc limit ? offset ?', (stime, pager['qnty'], (pager['page']-1)*pager['qnty'], ))
            posts = cur_posts.fetchall()

            if self.input('page', None) is None:
                _top = True

        ptids = {}
        ptags = {}
        psers = {}
        if posts:
            pager['list'] = len(posts)

            cur_posts.execute('select post_id,term_id from post_terms where post_id in (' + ','.join(str(i['post_id']) for i in posts) + ')')
            ptids = cur_posts.fetchall()
            if ptids:
                cur_terms.execute('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
                ptags = self.utils().array_keyto(cur_terms.fetchall(), 'term_id')
            ptids = self.utils().array_group(ptids, 'post_id')

            cur_users.execute('select * from users where user_id in (' + ','.join(str(i['user_id']) for i in posts) + ')')
            psers = self.utils().array_keyto(cur_users.fetchall(), 'user_id')

        cur_terms.execute('select * from terms where term_refc>0 order by term_refc desc, term_id desc limit 32')
        keyws_tag = cur_terms.fetchall()

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? and post_rank>=? order by post_rank desc, post_id desc limit 9', (stime, self.get_runtime_conf('index_posts_top_rank')))
        posts_top = cur_posts.fetchall()

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? order by post_refc desc, post_id desc limit 9', (stime,))
        posts_hot = cur_posts.fetchall()

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? order by post_ptms desc, post_id desc limit 9', (stime,))
        posts_new = cur_posts.fetchall()

        cur_posts.close()
        cur_terms.close()
        cur_users.close()

        cur_talks = self.dbase('talks').cursor()
        cur_talks.execute('select * from talks where talk_rank>=? order by talk_id desc limit 9', (self.get_runtime_conf('posts_talks_min_rank'), ))
        talks_new = cur_talks.fetchall()
        cur_talks.close()

        if _top:
            cur_links = self.dbase('links').cursor()
            cur_links.execute('select * from links where link_rank>=? order by link_rank desc, link_id desc limit 99', (self.get_runtime_conf('index_links_min_rank'), ))
            links_top = cur_links.fetchall()
            cur_links.close()
        else:
            links_top = None

        slabs_top = self.get_runtime_conf('slabs', json = True)

        self.render('posts.html', track = track, pager = pager, posts = posts, psers = psers, ptids = ptids, ptags = ptags
                , posts_top = posts_top, posts_hot = posts_hot, posts_new = posts_new
                , slabs_top = slabs_top, keyws_tag = keyws_tag, talks_new = talks_new, links_top = links_top)


class PostCtrl(BasicCtrl):
    def get(self, post_id):
        stime = self.stime()

        cur_posts = self.dbase('posts').cursor()
        cur_posts.execute('select * from posts where post_id = ?', (post_id, ))

        post = cur_posts.fetchone()

        if not post or ((not self.get_current_user()) and (not post['post_stat'] or post['post_ptms'] >= stime)):
            cur_posts.close()
            return self.send_error(404)

        cur_terms = self.dbase('terms').cursor()
        cur_users = self.dbase('users').cursor()

        ptids = {}
        ptags = {}
        psers = {}
        if post:
            cur_posts.execute('select post_id,term_id from post_terms where post_id = ?', (post_id, ))
            ptids = cur_posts.fetchall()
            if ptids:
                cur_terms.execute('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
                ptags = self.utils().array_keyto(cur_terms.fetchall(), 'term_id')
            ptids = self.utils().array_group(ptids, 'post_id')

            cur_users.execute('select * from users where user_id=?', (post['user_id'], ))
            psers = self.utils().array_keyto(cur_users.fetchall(), 'user_id')

        cur_posts.execute('select post_id from posts where post_stat>0 and post_ptms<? and post_id<? order by post_id desc limit 1', (stime, post_id, ))
        post_prev = cur_posts.fetchone()
        if post_prev:
            post_prev = post_prev['post_id']
        else:
            post_prev = 0

        cur_posts.execute('select post_id from posts where post_stat>0 and post_ptms<? and post_id>? order by post_id asc limit 1', (stime, post_id, ))
        post_next = cur_posts.fetchone()
        if post_next:
            post_next = post_next['post_id']
        else:
            post_next = 0

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? and post_rank>=? order by post_rank desc, post_id desc limit 9', (stime, self.get_runtime_conf('index_posts_top_rank')))
        posts_top = cur_posts.fetchall()

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? order by post_refc desc, post_id desc limit 9', (stime,))
        posts_hot = cur_posts.fetchall()

        cur_posts.execute('select post_id,post_title,post_descp from posts where post_stat>0 and post_ptms<? order by post_ptms desc, post_id desc limit 9', (stime,))
        posts_new = cur_posts.fetchall()

        cur_terms.execute('select * from terms where term_refc>0 order by term_refc desc, term_id desc limit 32')
        keyws_tag = cur_terms.fetchall()

        cur_posts.close()
        cur_terms.close()
        cur_users.close()

        cur_talks = self.dbase('talks').cursor()

        cur_talks.execute('select * from talks where talk_rank>=? order by talk_id desc limit 9', (self.get_runtime_conf('posts_talks_min_rank'), ))
        talks_new = cur_talks.fetchall()

        cur_talks.execute('select * from talks where post_id=? and talk_rank>=? order by talk_id asc', (post['post_id'], self.get_runtime_conf('posts_talks_min_rank')))
        talks = cur_talks.fetchall()

        cur_talks.close()

        slabs_top = self.get_runtime_conf('slabs', json = True)

        links_top = None

        self.render('post.html', post = post, psers = psers, ptids = ptids, ptags = ptags, talks = talks
                , post_prev = post_prev, post_next = post_next
                , posts_top = posts_top, posts_hot = posts_hot, posts_new = posts_new
                , slabs_top = slabs_top, keyws_tag = keyws_tag, talks_new = talks_new, links_top = links_top)
