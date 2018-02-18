# -*- coding: UTF-8 -*-

from app.ctrls.hello import HelloCtrl
from app.ctrls.error import ErrorCtrl

from app.ctrls.about import AboutCtrl
from app.ctrls.apply import ApplyCtrl
from app.ctrls.email import EmailCtrl
from app.ctrls.links import LinksCtrl
from app.ctrls.score import ScoreCtrl
from app.ctrls.talks import TalksCtrl
from app.ctrls.voice import VoiceCtrl
from app.ctrls.posts import PostsCtrl, PostCtrl

from app.ctrls.check import CheckCtrl

from app.ctrls.login import LoginCtrl
from app.ctrls.leave import LeaveCtrl

from app.ctrls.shell.index import Shell_IndexCtrl
from app.ctrls.shell.panel import Shell_PanelCtrl

from app.ctrls.admin.index import Admin_IndexCtrl
from app.ctrls.admin.cache import Admin_CacheCtrl, Admin_CacheDeleteCtrl
from app.ctrls.admin.files import Admin_FilesCtrl, Admin_FileCtrl, Admin_FileUploadCtrl, Admin_FileDeleteCtrl
from app.ctrls.admin.confs import Admin_ConfsCtrl, Admin_ConfCtrl, Admin_ConfCreateCtrl, Admin_ConfDeleteCtrl
from app.ctrls.admin.posts import Admin_PostsCtrl, Admin_PostCtrl, Admin_PostCreateCtrl, Admin_PostHiddenCtrl
from app.ctrls.admin.links import Admin_LinksCtrl, Admin_LinkCtrl, Admin_LinkCreateCtrl, Admin_LinkDeleteCtrl
from app.ctrls.admin.talks import Admin_TalksCtrl, Admin_TalkCtrl, Admin_TalkDeleteCtrl
from app.ctrls.admin.mails import Admin_MailsCtrl, Admin_MailAccessCtrl, Admin_MailDeleteCtrl, Admin_MailResendCtrl
from app.ctrls.admin.terms import Admin_TermsCtrl, Admin_TermCtrl, Admin_TermCreateCtrl
from app.ctrls.admin.users import Admin_UsersCtrl, Admin_UserCtrl, Admin_UserCreateCtrl
from app.ctrls.admin.alogs import Admin_AlogsCtrl

url = [
    (r'/', PostsCtrl),

    (r'/s', PostsCtrl),
    (r'/t/([^/]+)', PostsCtrl),
    (r'/p/([1-9][0-9]*)', PostCtrl),

    (r'/hello', HelloCtrl),
    (r'/about', AboutCtrl),
    (r'/apply', ApplyCtrl),
    (r'/email', EmailCtrl),
    (r'/links', LinksCtrl),
    (r'/score', ScoreCtrl),
    (r'/voice', VoiceCtrl),
    (r'/talks(\.json)', TalksCtrl),

    (r'/check(\.jpeg)', CheckCtrl),

    (r'/login', LoginCtrl),
    (r'/leave', LeaveCtrl),

    (r'/shell', Shell_PanelCtrl),
    (r'/@([^/]+)', Shell_IndexCtrl),

    (r'/admin', Admin_IndexCtrl),

    (r'/admin/alogs', Admin_AlogsCtrl),

    (r'/admin/confs', Admin_ConfsCtrl),
    (r'/admin/conf', Admin_ConfCtrl),
    (r'/admin/conf/create', Admin_ConfCreateCtrl),
    (r'/admin/conf/delete', Admin_ConfDeleteCtrl),

    (r'/admin/files', Admin_FilesCtrl),
    (r'/admin/file', Admin_FileCtrl),
    (r'/admin/file/upload', Admin_FileUploadCtrl),
    (r'/admin/file/delete', Admin_FileDeleteCtrl),

    (r'/admin/links', Admin_LinksCtrl),
    (r'/admin/link', Admin_LinkCtrl),
    (r'/admin/link/create', Admin_LinkCreateCtrl),
    (r'/admin/link/delete', Admin_LinkDeleteCtrl),

    (r'/admin/mails', Admin_MailsCtrl),
    (r'/admin/mail/access', Admin_MailAccessCtrl),
    (r'/admin/mail/delete', Admin_MailDeleteCtrl),
    (r'/admin/mail/resend', Admin_MailResendCtrl),

    (r'/admin/posts', Admin_PostsCtrl),
    (r'/admin/post', Admin_PostCtrl),
    (r'/admin/post/create', Admin_PostCreateCtrl),
    (r'/admin/post/hidden', Admin_PostHiddenCtrl),

    (r'/admin/talks', Admin_TalksCtrl),
    (r'/admin/talk', Admin_TalkCtrl),
    (r'/admin/talk/delete', Admin_TalkDeleteCtrl),

    (r'/admin/terms', Admin_TermsCtrl),
    (r'/admin/term', Admin_TermCtrl),
    (r'/admin/term/create', Admin_TermCreateCtrl),

    (r'/admin/users', Admin_UsersCtrl),
    (r'/admin/user', Admin_UserCtrl),
    (r'/admin/user/create', Admin_UserCreateCtrl),

    (r'/admin/cache', Admin_CacheCtrl),
    (r'/admin/cache/delete', Admin_CacheDeleteCtrl),

    (r'.*', ErrorCtrl)
]
