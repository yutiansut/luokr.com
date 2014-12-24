luokr.com
=========

The initial version of luokr.com was developed by Alvan in July 2013. It is a Python-based server application using Tornado framework at backend and Bootstrap framework at frontend.
Now it just a simple blog about technology and life.


Below is the main directory structure:

    res.luokr.com/      # global resources
    www.luokr.com/
    ---- app/
    -------- etc.py     # configuration file, see `doc/etc.py.sample` for more details
    -------- svr.py     # to start the app, run `python svr.py`
    -------- url.py     # url mapping
    -------- ctrls/     # controllers, see Tornado's RequestHandler
    -------- datas/     # data files
    -------- model/     # model class files
    -------- views/     # templates
    ---- doc/           # documents
    ---- lib/           # library files
    ---- www/           # static files



The background landing address is `/admin`, default username is `admin` and the password is `888888`.
You can change it after you logined.

Requirement
------------

(Python >= 2.7)

* tornado (>= 3.1.1)
* pil or pillow


Screenshots
-----------

posts:
![www.luokr.com.posts.png](res.luokr.com/img/20140530/www.luokr.com.posts.png)

about:
![www.luokr.com.about.png](res.luokr.com/img/20140216/www.luokr.com.about.png)

login:
![www.luokr.com.login.png](res.luokr.com/img/20140530/www.luokr.com.login.png)

admin:
![www.luokr.com.admin.png](res.luokr.com/img/20140415/www.luokr.com.admin.png)

admin edit post:
![www.luokr.com.admin.post.update.png](res.luokr.com/img/20140415/www.luokr.com.admin.post.update.png)

