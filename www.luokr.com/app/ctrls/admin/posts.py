#coding=utf-8

from admin import admin, AdminCtrl

class Admin_PostsCtrl(AdminCtrl):
    @admin
    def get(self):
        pager = {}
        pager['qnty'] = min(int(self.input('qnty', 10)), 50)
        pager['page'] = max(int(self.input('page', 1)), 1)
        pager['list'] = 0;

        cur_posts = self.dbase('posts').cursor()
        cur_users = self.dbase('users').cursor()

        cur_posts.execute('select * from posts order by post_id desc limit ? offset ?', (pager['qnty'], (pager['page']-1)*pager['qnty'], ))
        posts = cur_posts.fetchall()

        psers = {}
        if posts:
            pager['list'] = len(posts)

            cur_users.execute('select * from users where user_id in (' + ','.join(str(i['user_id']) for i in posts) + ')')
            psers = self.utils().array_keyto(cur_users.fetchall(), 'user_id')

        cur_posts.close()
        cur_users.close()
        self.render('admin/posts.html', pager = pager, posts = posts, psers = psers)

class Admin_PostHiddenCtrl(AdminCtrl):
    @admin
    def post(self):
        try:
            post_id = self.input('post_id')

            con = self.dbase('posts')
            cur = con.cursor()
            cur.execute('update posts set post_stat = 0 where post_id = ?', (post_id, ))
            con.commit()
            cur.close()
            self.flash(1)
        except:
            self.flash(0)

class Admin_PostCreateCtrl(AdminCtrl):
    @admin
    def get(self):
        cur = self.dbase('terms').cursor()

        cur.execute('select * from terms order by term_id desc, term_refc desc limit 9')
        terms = cur.fetchall()
        cur.close()

        mode = self.input('mode', None)

        self.render('admin/post-create.html', mode = mode, terms = terms)

    @admin
    def post(self):
        try:
            user = self.current_user

            post_type    = self.input('post_type', 'blog')
            post_title   = self.input('post_title')
            post_descp   = self.input('post_descp')
            post_author  = self.input('post_author')
            post_source  = self.input('post_source')
            post_summary = self.input('post_summary')
            post_content = self.input('post_content')

            post_rank = self.input('post_rank')
            post_stat = self.input('post_stat', 0)
            post_ptms = int(self.timer().mktime(self.timer().strptime(self.input('post_ptms'), '%Y-%m-%d %H:%M:%S')))
            post_ctms = self.stime()
            post_utms = post_ctms

            term_list = []
            for term_name in self.input('term_list').split(' '):
                if term_name == '':
                    continue
                term_list.append(term_name)

            if len(term_list) > 10:
                self.flash(0, {'msg': '标签数量限制不能超过 10 个'})
                return

            con_posts = self.dbase('posts')
            cur_posts = con_posts.cursor()

            con_terms = self.dbase('terms')
            cur_terms = con_terms.cursor()

            term_imap = {}
            term_ctms = self.stime()
            for term_name in term_list:
                cur_terms.execute('select term_id from terms where term_name = ?', (term_name ,))
                term_id = cur_terms.fetchone()
                if term_id:
                    term_id = term_id['term_id']
                else:
                    cur_terms.execute('insert or ignore into terms (term_name, term_ctms) values (?, ?)', (term_name , term_ctms, ))
                    if cur_terms.lastrowid:
                        term_id = cur_terms.lastrowid

                if term_id:
                    term_imap[term_id] = term_name

            cur_posts.execute('insert into posts (user_id, post_type, post_title, post_descp, post_author, post_source, post_summary, post_content,post_stat, post_rank, post_ptms, post_ctms, post_utms) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                    (user['user_id'], post_type, post_title, post_descp, post_author, post_source, post_summary, post_content, post_stat, post_rank, post_ptms, post_ctms, post_utms ,))
            post_id = cur_posts.lastrowid

            if term_imap:
                for term_id in term_imap:
                    cur_posts.execute('insert or ignore into post_terms (post_id, term_id) values (' + str(post_id) + ',' + str(term_id) + ')')

            if term_imap:
                cur_terms.execute('update terms set term_refc = term_refc + 1 where term_id in (' + ','.join([str(i) for i in term_imap.keys()]) + ')')

            con_posts.commit()
            cur_posts.close()

            con_terms.commit()
            con_terms.close()

            self.model('alogs').add(self.dbase('alogs'), '新增文章：' + str(post_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
            self.flash(1, {'url': '/admin/post?post_id=' + str(post_id)})
        except:
            self.flash(0)


class Admin_PostCtrl(AdminCtrl):
    @admin
    def get(self):
        post_id = self.input('post_id')

        con_posts = self.dbase('posts')
        cur_posts = con_posts.cursor()

        cur_posts.execute('select * from posts where post_id = ?', (post_id, ))
        post = cur_posts.fetchone()
        if not post:
            cur_posts.close()
            return self.send_error(404)

        mode = self.input('mode', None)

        con_terms = self.dbase('terms')
        cur_terms = con_terms.cursor()

        cur_terms.execute('select * from terms order by term_id desc, term_refc desc limit 9')
        terms = cur_terms.fetchall()

        ptids = {}
        ptags = {}

        cur_posts.execute('select post_id,term_id from post_terms where post_id = ?', (post_id, ))
        ptids = cur_posts.fetchall()
        if ptids:
            cur_terms.execute('select * from terms where term_id in (' + ','.join(str(i['term_id']) for i in ptids) + ')')
            ptags = cur_terms.fetchall()
            if ptags:
                ptids = self.utils().array_group(ptids, 'post_id')
                ptags = self.utils().array_keyto(ptags, 'term_id')

        cur_posts.close()
        cur_terms.close()

        self.render('admin/post.html', mode = mode, post = post, terms = terms, ptids = ptids, ptags = ptags)

    @admin
    def post(self):
        try:
            user = self.current_user

            post_id      = self.input('post_id')
            post_title   = self.input('post_title')
            post_descp   = self.input('post_descp')
            post_author  = self.input('post_author')
            post_source  = self.input('post_source')
            post_summary = self.input('post_summary')
            post_content = self.input('post_content')

            post_rank = self.input('post_rank')
            post_stat = self.input('post_stat', 0)
            post_ptms = int(self.timer().mktime(self.timer().strptime(self.input('post_ptms'), '%Y-%m-%d %H:%M:%S')))
            post_utms = self.stime()

            term_list = []
            for term_name in self.input('term_list').split(' '):
                if term_name == '':
                    continue
                term_list.append(term_name)

            if len(term_list) > 10:
                self.flash(0, {'msg': '标签数量限制不能超过 10 个'})
                return

            con_posts = self.dbase('posts')
            cur_posts = con_posts.cursor()

            con_terms = self.dbase('terms')
            cur_terms = con_terms.cursor()

            cur_posts.execute('select * from posts where post_id = ?', (post_id, ))
            post = cur_posts.fetchone()
            if not post:
                cur_posts.close()
                cur_terms.close()
                self.flash(0, '没有指定文章ID')
                return

            term_imap = {}
            term_ctms = self.stime()
            for term_name in term_list:
                cur_terms.execute('select term_id from terms where term_name = ?', (term_name ,))
                term_id = cur_terms.fetchone()
                if term_id:
                    term_id = term_id['term_id']
                else:
                    cur_terms.execute('insert or ignore into terms (term_name, term_ctms) values (?, ?)', (term_name , term_ctms, ))
                    if cur_terms.lastrowid:
                        term_id = cur_terms.lastrowid

                if term_id:
                    term_imap[term_id] = term_name

            cur_posts.execute('select term_id from post_terms where post_id = ?', (post_id, ))
            post_tids = cur_posts.fetchall()

            cur_posts.execute('update posts set user_id=?,post_title=?,post_descp=?,post_author=?,post_source=?,post_summary=?,post_content=?,post_stat=?,post_rank=?,post_ptms=?,post_utms=? where post_id=?', \
                    (user['user_id'], post_title, post_descp, post_author, post_source, post_summary, post_content, post_stat, post_rank, post_ptms, post_utms, post_id,))
            cur_posts.execute('delete from post_terms where post_id = ?', (post_id,))

            if term_imap:
                for term_id in term_imap:
                    cur_posts.execute('insert or ignore into post_terms (post_id, term_id) values (' + str(post_id) + ',' + str(term_id) + ')')

            if post_tids:
                cur_terms.execute('update terms set term_refc = term_refc - 1 where term_id in (' + ','.join([str(i['term_id']) for i in post_tids]) + ')')
            if term_imap:
                cur_terms.execute('update terms set term_refc = term_refc + 1 where term_id in (' + ','.join([str(i) for i in term_imap.keys()]) + ')')

            con_posts.commit()
            cur_posts.close()

            con_terms.commit()
            cur_terms.close()

            self.model('alogs').add(self.dbase('alogs'), '更新文章：' + str(post_id), user_ip = self.request.remote_ip, user_id = user['user_id'], user_name = user['user_name'])
            self.flash(1)
        except:
            self.flash(0)
