luokr.com
=========

螺壳网最初的版本(V0.3)是在 2013年7月 由 Alvan 开发， 基于 Python 服务端框架 Tornado ，前端框架使用 Bootstrap。 目前看来只是一个简单的科技 | 生活博客，以后会发展成为什么样？我们也还不知道。


####螺壳网源代码(V0.3)

仅是一个实验版本！

主要目录结构如下：

    res.luokr.com/
    www.luokr.com/V0.3
    ---- app/           #应用目录
    -------- etc.py     #应用配置，该文件可以参考 doc/etc.py.sample 的配置
    -------- svr.py     #服务入口，启动服务：python svr.py
    -------- url.py     #路由配置
    -------- ctrls/     #控制器文件(Tornado的RequestHandler)
    -------- datas/     #数据文件，SQLite3数据库文件目录，带建表语句
    -------- model/     #模型文件
    -------- views/     #视图文件
    ---- doc/           #文档目录
    ---- lib/           #类库文件
    ---- www/           #WEB根目录


关于数据库，这个版本使用SQLite3，
请使用 app/datas 目录下的.sql文件建立各数据库，

后台登陆地址为/login，users库的主表users默认用户名 admin，密码888888，登录后台可自行修改。


后台管理-控制面板页面截图：
![后台管理-控制面板页面](http://res.luokr.com/img/20140415/www.luokr.com.admin.png)

后台管理-文章编辑页面截图：
![后台管理-文章编辑页面](http://res.luokr.com/img/20140415/www.luokr.com.admin.post.update.png)

日志列表页面截图：
![日志列表页面](http://res.luokr.com/img/20140216/www.luokr.com.posts.png)

关于我们页面截图：
![关于我们页面](http://res.luokr.com/img/20140216/www.luokr.com.about.png)
