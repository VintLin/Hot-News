import hashlib

import bleach
from markdown import markdown

from vSQL.vorm import Module
from vSQL.vattr import *
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from App import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from App.tool.ip import *


@login_manager.user_loader
def load_user(user_id):
    account = Account()
    account.id = user_id
    account.select(getone=True)
    return account


OPERATE = ['评论', '点赞', '收藏', '浏览', '文章', '关注']


class Operand:  # 对象
    NEWS = 0
    POST = 1
    COMMENT = 2
    USER = 3
    INDEX = 4


class Operate:  # 操作
    COMMENT = 0
    LIKE = 1
    COLLECT = 2
    BROWSE = 3
    POST = 4
    FOLLOW = 5


# don't change
class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(Module):
    id = column(zintger(), isAutocount=True, isPrimary=True)
    name = column(zchar(64), isUnique=True)
    tacit = column(zbool(default=False))
    permissions = column(zintger())

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator': [Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role(name=r).select(getone=True)
            if not role.id:
                role.reset_permissions()
                for perm in roles[r]:
                    role.add_permission(perm)
                role.tacit = (role.name == default_role)
                role.insert()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class Visitor(Module):
    id = column(zintger(), isAutocount=True, isPrimary=True)
    ip = column(zchar(20))
    site = column(zchar(30))
    member_since = column(zdatetime())
    again_since = column(zdatetime())
    browse = column(zintger(default=0))

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.member_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.site = find(self.ip)

    def ping(self):
        self.member_since = None
        self.again_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.browse = int(self.browse) + 1
        self.update()


class Account(Module, UserMixin):
    id = column(zintger(20), isAutocount=True, isPrimary=True, isNotnull=True)
    email = column(zchar(30), isNotnull=True)
    account = column(zchar(30), isNotnull=True)
    password_hash = column(zchar(128), isNotnull=True)
    confirmed = column(zbool(default=False), isNotnull=True)
    role_id = column(zintger(20))
    member_since = column(zdatetime())
    last_seen = column(zdatetime())
    browse = column(zintger(default=0))
    foreign_key = foreign('role_id', 'Role', 'id')

    def listener_begin(self, do):
        if do is Module.M_UPDATE:
            self.member_since = None
        elif do is Module.M_INSERT:
            role = Role()
            if self.email == current_app.config['NEWS_ADMIN']:
                role.permissions = 0xff
                role.select(getone=True)
                self.role_id = role.id
            else:
                role.tacit = True
                role.select(getone=True)
                self.role_id = role.id
            self.member_since = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def listener_end(self, do):
        if do is Module.M_INSERT:
            Info(id=self.id, name=self.account, avatar_hash=self.gravatar_hash()).insert()
        if do is Module.M_SELECT:
            self.info = Info(id=self.id).select(getone=True)

    def ping(self):
        self.last_seen = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.update()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        account = Account()
        account.id = data.get('reset')
        account.select(getone=True)
        if account.email is None:
            return False
        account.password = new_password
        account.update()
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps(
            {'change_email': self.id, 'new_email': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.email == new_email:
            return False
        self.email = new_email
        info = Info(id=self.id).select(getone=True)
        info.avatar_hash = self.gravatar_hash()
        info.update()
        self.update()
        return True

    def can(self, perm):
        role = Role(id=self.role_id).select(getone=True)
        return role is not None and role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def follow(self, user):
        Follow(follower=self.id, befollow=user.id).insert()

    def unfollow(self, user):
        Follow(follower=self.id, befollow=user.id).delete()

    def is_follow(self, user):
        f = Follow(follower=self.id, befollow=user.id).select(getone=True)
        return bool(f.timestamp)

    def get_follower(self, getcount=False):
        follows = Follow(befollow=self.id).select(oderby="timestamp", isasc=False)
        users = []
        if getcount:
            return len(follows)
        else:
            for follow in follows:
                users.append(Info(id=follow.follower).select(getone=True))
            return users

    def get_follow(self, getcount=False):
        follows = Follow(follower=self.id).select(oderby="timestamp", isasc=False)
        users = []
        if getcount:
            return len(follows)
        else:
            for follow in follows:
                users.append(Info(id=follow.befollow).select(getone=True))
            return users

    def browse_it(self, user_id):
        History().record(user_id, self.id, Operand.USER, Operate.BROWSE)
        Account(id=self.id, browse=int(self.browse) + 1).update()

    def __repr__(self):
        return '<Account %r>' % self.account


class Info(Module):
    id = column(zintger(20))
    avatar_hash = column(zchar(32))
    name = column(zchar(20), isNotnull=True)
    realname = column(zchar(40))
    about_me = column(zchar(200))
    sex = column(zchar(4))
    birthday = column(zdate())
    hometown = column(zchar(100))
    location = column(zchar(100))
    job = column(zchar(100))
    company = column(zchar(100))
    school = column(zchar(100))
    phone = column(zchar(20))
    foreign_key = foreign('id', 'Account', 'id')

    def gravatar(self, size=100, default='identicon', rating='g'):
        url = 'https://secure.gravatar.com/avatar'
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=self.avatar_hash, size=size, default=default, rating=rating)


class News(Module):
    id = column(zintger(20), isAutocount=True, isPrimary=True, isNotnull=True)
    filename = column(zchar(80), isNotnull=True)
    path = column(zchar(100), isNotnull=True)
    image = column(zchar(150))
    website = column(zchar(20), isNotnull=True)
    title = column(zchar(80), isNotnull=True)
    time = column(zdatetime(), isNotnull=True)
    type = column(zchar(20), isNotnull=True)
    browse = column(zintger(default=0))
    thumb = column(zintger(default=0))
    collect = column(zintger(default=0))

    def insert(self):
        news = News(title=self.title).select(getone=True)
        if not news.id:
            super(News, self).insert_without_return()
        else:
            print("news already existed")

    def browse_it(self, user_id):
        History().record(user_id, self.id, Operand.NEWS, Operate.BROWSE)
        News(id=self.id, browse=int(self.browse) + 1).update()

    def set_comment(self, body, user_id):
        return Comment(body=body, user_id=user_id, operand=Operand.NEWS, operand_id=self.id).insert()

    def del_comment(self, user_id):
        return Comment(user_id=user_id, operand=Operand.NEWS, operand_id=self.id).delete()

    def is_thumb(self, user_id):
        t = Thumb(user_id=user_id, operand=Operand.NEWS, operand_id=self.id).select(getone=True)
        if t.id:
            return 1
        else:
            return 0

    def set_thumb(self, user_id):
        self.thumb = int(self.thumb) + 1
        News(id=self.id, thumb=self.thumb).update()
        return Thumb(user_id=user_id, operand=Operand.NEWS, operand_id=self.id).insert()

    def del_thumb(self, user_id):
        self.thumb = int(self.thumb) - 1
        News(id=self.id, thumb=self.thumb).update()
        return Thumb(user_id=user_id, operand=Operand.NEWS, operand_id=self.id).delete()

    def is_collect(self, user_id):
        t = Collect(user_id=user_id, operand=Operand.NEWS, operand_id=self.id).select(getone=True)
        if t.id:
            return 1
        else:
            return 0

    def set_collect(self, usr_id):
        self.collect = int(self.collect) + 1
        News(id=self.id, collect=self.collect).update()
        Collect(user_id=usr_id, operand=Operand.NEWS, operand_id=self.id).insert()

    def del_collect(self, usr_id):
        self.collect = int(self.collect) - 1
        News(id=self.id, collect=self.collect).update()
        Collect(user_id=usr_id, operand=Operand.NEWS, operand_id=self.id).delete()

    @staticmethod
    def get_oper():
        return Operand.NEWS


class Post(Module):
    id = column(zintger(), isPrimary=True, isAutocount=True, isNotnull=True)
    user_id = column(zintger())
    path = column(zchar(100))
    title = column(zchar(100))
    type = column(zchar(20), isNotnull=True)
    body = column(ztext())
    body_html = column(ztext())
    timestamp = column(zdatetime())
    publish = column(zbool())
    browse = column(zintger(default=0))
    thumb = column(zintger(default=0))
    collect = column(zintger(default=0))
    foreign_key = foreign('user_id', 'Info', 'id')

    def __init__(self, **args):
        self.info = None
        super().__init__(**args)

    def get_user(self):
        return Info(id=self.user_id).select(getone=True)

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            Post.on_changed_body(target=self, value=self.body)
        if do is Module.M_UPDATE:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if self.body:
                Post.on_changed_body(target=self, value=self.body)
        if do is Module.M_DELETE:
            Thumb(operand=Operand.POST, operand_id=self.id).delete()
            Comment(operand=Operand.POST, operand_id=self.id).delete()
            History(operand=Operand.POST, operand_id=self.id).delete()

    def listener_end(self, do):
        if do is Module.M_INSERT:
            Post(id=self.id, path='/{}/{}/{}'.format('post', str(self.timestamp)[:10], self.id)).update()
        if do is Module.M_SELECT:
            self.info = Info(id=self.user_id).select(getone=True)

    def browse_it(self):
        History().record(self.user_id, self.id, Operand.POST, Operate.BROWSE)
        Post(id=self.id, browse=int(self.browse) + 1).update()

    def set_comment(self, body, user_id):
        return Comment(body=body, user_id=user_id, operand=Operand.POST, operand_id=self.id).insert()

    def del_comment(self, user_id):
        return Comment(user_id=user_id, operand=Operand.POST, operand_id=self.id).delete()

    def is_thumb(self, user_id):
        t = Thumb(user_id=user_id, operand=Operand.POST, operand_id=self.id).select(getone=True)
        if t.id:
            return 1
        else:
            return 0

    def set_thumb(self, usr_id):
        self.thumb = int(self.thumb) + 1
        Post(id=self.id, thumb=self.thumb).update()
        Thumb(user_id=usr_id, operand=Operand.POST, operand_id=self.id).insert()

    def del_thumb(self, usr_id):
        self.thumb = int(self.thumb) - 1
        Post(id=self.id, thumb=self.thumb).update()
        Thumb(user_id=usr_id, operand=Operand.POST, operand_id=self.id).delete()

    def is_collect(self, user_id):
        t = Collect(user_id=user_id, operand=Operand.POST, operand_id=self.id).select(getone=True)
        if t.id:
            return 1
        else:
            return 0

    def set_collect(self, usr_id):
        self.collect = int(self.collect) + 1
        Post(id=self.id, collect=self.collect).update()
        Collect(user_id=usr_id, operand=Operand.POST, operand_id=self.id).insert()

    def del_collect(self, usr_id):
        self.collect = int(self.collect) - 1
        Post(id=self.id, collect=self.collect).update()
        Collect(user_id=usr_id, operand=Operand.POST, operand_id=self.id).delete()

    @staticmethod
    def on_changed_body(target, value):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'br',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'),
                                                       tags=allowed_tags,
                                                       strip=True))

    @staticmethod
    def get_oper():
        return Operand.POST


class Comment(Module):
    id = column(zintger(), isPrimary=True, isAutocount=True, isNotnull=True)
    body = column(zchar(255))
    user_id = column(zintger())
    operand = column(zintger(default=0))
    operand_id = column(zintger())
    timestamp = column(zdatetime())

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def listener_end(self, do):
        if do is Module.M_INSERT:
            History().record(self.user_id, self.operand_id, self.operand, Operate.COMMENT)
        if do is Module.M_DELETE:
            History().delete_record(self.user_id, self.operand_id, self.operand, Operate.COMMENT)

    @staticmethod
    def get_oper():
        return Operand.COMMENT


OPERAND = [News, Post, Comment, Account]


class Thumb(Module):
    id = column(zintger(), isPrimary=True, isAutocount=True, isNotnull=True)
    user_id = column(zintger())
    operand = column(zintger())
    operand_id = column(zintger())
    timestamp = column(zdatetime())
    foreign_key = foreign('user_id', 'Info', 'id')

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def listener_end(self, do):
        if do is Module.M_INSERT:
            History().record(self.user_id, self.operand_id, self.operand, Operate.LIKE)
        if do is Module.M_DELETE:
            History().delete_record(self.user_id, self.operand_id, self.operand, Operate.LIKE)


class Collect(Module):
    id = column(zintger(), isPrimary=True, isAutocount=True, isNotnull=True)
    collect_name = column(zchar(30))
    user_id = column(zintger())
    operand = column(zintger())
    operand_id = column(zintger())
    timestamp = column(zdatetime())
    foreign_key = foreign('user_id', 'Info', 'id')

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def listener_end(self, do):
        if do is Module.M_INSERT:
            History().record(self.user_id, self.operand_id, self.operand, Operate.COLLECT)
        if do is Module.M_DELETE:
            History().delete_record(self.user_id, self.operand_id, self.operand, Operate.COLLECT)


class Follow(Module):
    befollow = column(zintger(), isNotnull=True)
    follower = column(zintger(), isNotnull=True)
    timestamp = column(zdatetime())

    def insert(self):
        if self.befollow == self.follower:
            return False
        else:
            super(Follow, self).insert()

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class History(Module):
    user_id = column(zintger())
    operand_id = column(zintger(), isNotnull=True)
    operand = column(zintger(3, default=0), isNotnull=True)
    operate = column(zintger(3, default=0), isNotnull=True)
    timestamp = column(zdatetime(), isNotnull=True)
    path = column(zchar(100), isNotnull=True)
    title = column(zchar(100), isNotnull=True)
    message = column(zchar(100))

    @staticmethod
    def record(user_id, operand_id, operand, operate):
        print("RECORD", user_id, operand_id, operand, operate)
        history = History(user_id=user_id, operand_id=operand_id, operand=operand, operate=operate)
        history.set_period(field='timestamp', time_slot='-12:00:00').delete()
        history.insert()

    @staticmethod
    def delete_record(user_id, operand_id, operand, operate):
        History(user_id=user_id, operand_id=operand_id, operand=operand, operate=operate).delete()

    def listener_begin(self, do):
        if do is Module.M_INSERT:
            self.timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if self.operand is Operand.NEWS:
                news = News(id=self.operand_id).select(getone=True)
                self.path = news.path
                self.title = news.title
            if self.operand is Operand.POST:
                post = Post(id=self.operand_id).select(getone=True)
                self.path = post.path
                self.title = post.title
            if self.operand is Operand.USER:
                user = Account(id=self.operand_id).select(getone=True)
                self.path = "/user/"+user.account
                self.title = user.account+"的主页"
            if self.operand is Operand.COMMENT:
                pass

    def get_oper(self):
        return OPERATE[self.operate]


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonymousUser
