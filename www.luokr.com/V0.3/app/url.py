#coding=utf-8

from ctrls.hello import HelloCtrl
from ctrls.error import ErrorCtrl
from ctrls.about import AboutCtrl
from ctrls.apply import ApplyCtrl
from ctrls.email import EmailCtrl
from ctrls.voice import VoiceCtrl
from ctrls.links import LinksCtrl
from ctrls.posts import PostsCtrl, PostCtrl

from ctrls.login import LoginCtrl
from ctrls.leave import LeaveCtrl

from ctrls.panel import PanelCtrl

from ctrls.image import ImageRandomCtrl

from ctrls.admin.index import Admin_IndexCtrl
from ctrls.admin.cache import Admin_CacheCtrl, Admin_CacheDeleteCtrl
from ctrls.admin.image import Admin_ImageUploadCtrl
from ctrls.admin.confs import Admin_ConfsCtrl, Admin_ConfCtrl, Admin_ConfCreateCtrl, Admin_ConfDeleteCtrl, Admin_ConfReloadCtrl
from ctrls.admin.posts import Admin_PostsCtrl, Admin_PostCtrl, Admin_PostCreateCtrl, Admin_PostHiddenCtrl
from ctrls.admin.talks import Admin_TalksCtrl, Admin_TalkCtrl, Admin_TalkHiddenCtrl
from ctrls.admin.links import Admin_LinksCtrl, Admin_LinkCtrl, Admin_LinkCreateCtrl, Admin_LinkDeleteCtrl
from ctrls.admin.mails import Admin_MailsCtrl, Admin_MailAccessCtrl
from ctrls.admin.users import Admin_UsersCtrl
from ctrls.admin.terms import Admin_TermsCtrl, Admin_TermCtrl, Admin_TermCreateCtrl
from ctrls.admin.alogs import Admin_AlogsCtrl

url = [
    (r'/', PostsCtrl),

    (r'/hello', HelloCtrl),
    (r'/about', AboutCtrl),
    (r'/apply', ApplyCtrl),
    (r'/email', EmailCtrl),
    (r'/links', LinksCtrl),
    (r'/voice', VoiceCtrl),

    (r'/s', PostsCtrl),
    (r'/t/([^/]+)', PostsCtrl),
    (r'/p/([1-9][0-9]*)', PostCtrl),

    (r'/login', LoginCtrl),
    (r'/leave', LeaveCtrl),

    (r'/panel', PanelCtrl),

    (r'/image/random', ImageRandomCtrl),

    (r'/admin', Admin_IndexCtrl),

    (r'/admin/image/upload', Admin_ImageUploadCtrl),

    (r'/admin/confs', Admin_ConfsCtrl),
    (r'/admin/conf/create', Admin_ConfCreateCtrl),
    (r'/admin/conf/delete', Admin_ConfDeleteCtrl),
    (r'/admin/conf/reload', Admin_ConfReloadCtrl),
    (r'/admin/conf', Admin_ConfCtrl),

    (r'/admin/cache', Admin_CacheCtrl),
    (r'/admin/cache/delete', Admin_CacheDeleteCtrl),

    (r'/admin/posts', Admin_PostsCtrl),
    (r'/admin/post', Admin_PostCtrl),
    (r'/admin/post/create', Admin_PostCreateCtrl),
    (r'/admin/post/hidden', Admin_PostHiddenCtrl),

    (r'/admin/talks', Admin_TalksCtrl),
    (r'/admin/talk', Admin_TalkCtrl),
    (r'/admin/talk/hidden', Admin_TalkHiddenCtrl),

    (r'/admin/links', Admin_LinksCtrl),
    (r'/admin/link', Admin_LinkCtrl),
    (r'/admin/link/create', Admin_LinkCreateCtrl),
    (r'/admin/link/delete', Admin_LinkDeleteCtrl),

    (r'/admin/mails', Admin_MailsCtrl),
    (r'/admin/mail/access', Admin_MailAccessCtrl),
    (r'/admin/users', Admin_UsersCtrl),

    (r'/admin/terms', Admin_TermsCtrl),
    (r'/admin/term', Admin_TermCtrl),
    (r'/admin/term/create', Admin_TermCreateCtrl),

    (r'/admin/alogs', Admin_AlogsCtrl),

    (r'.*', ErrorCtrl)
]
