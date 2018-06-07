from flask import render_template, session, redirect, url_for, current_app, abort, flash, request
from flask_login import login_required, current_user
from App.decorators import admin_required
from . import main
from .forms import *
from Model.model import *
import json
import os


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    visitor = Visitor(ip=request.remote_addr).select(getone=True)
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))
    if visitor.id:
        visitor.ping()
    else:
        visitor.insert()

    with open('info/Frequency.json', 'r', encoding='utf-8') as f:
        wordDict = json.loads(f.read())

    news = []
    news_list = []
    with open('info/image.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i in range(len(lines)):
        if i < 3:
            news.append(News(id=str(lines[i])).select(getone=True))
        elif i < 70:
            news_list.append(News(id=str(lines[i])).select(getone=True))

    return render_template('/main/index.html',
                           wordDict=wordDict,
                           form=form,
                           news=news,
                           newsList=news_list)


@main.route('/search/<wd>/<int:page>', methods=['GET', 'POST'])
def search(wd, page):
    form = SearchForm()
    if form.validate_on_submit():
        nwd = form.search.data
        return redirect('/search/{}/1'.format(nwd))

    if wd is not None:
        form.search.data = wd

    pagination = News(title=wd).set_pagination(page=page, paging=20).select(islike=True, oderby='id')
    return render_template('/main/search.html',
                           wd=wd,
                           form=form,
                           pagination=pagination)


@main.route('/types', methods=['GET', 'POST'])
def type_list_page():
    form = SearchForm()
    typeList = []
    newsList = []
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))
    with open('info/TypeToTitle.json', 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())

    for k, v in typeDict.items():
        typeList.append(k)
        newsList.append(v)

    count = len(typeList)
    return render_template('/main/type-start.html',
                           typeList=typeList,
                           newsList=newsList,
                           len=count,
                           form=form)


@main.route('/<type>', methods=['GET', 'POST'])
def typePage(type):
    form = SearchForm()
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))

    with open('info/type/' + type + '.json', 'r', encoding='utf-8') as f:
        titleDict = json.loads(f.read())
    itemList = []
    for item in titleDict.values():
        itemList.append(item)
    return render_template('/main/type.html',
                           itemList=itemList,
                           type=type,
                           form=form,)


@main.route('/time/<int:page>', methods=['GET', 'POST'])
def timePage(page):
    form = SearchForm()
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))

    with open('info/times/'+str(page)+'.json', 'r', encoding='utf-8') as f:
        timesDict = json.loads(f.read())

    pages = len(os.listdir('info/times'))
    hasPrev = page is not 1
    hasNext = page is not pages - 1
    return render_template('/main/time.html',
                           timesDict=timesDict,
                           form=form,
                           page=page,
                           prevNum=page - 1,
                           nextNum=page + 1,
                           hasPrev=hasPrev,
                           hasNext=hasNext,
                           pages=pages)


@main.route('/user-post/<int:page>', methods=['GET'])
def posts(page):
    form = SearchForm()
    if form.validate_on_submit():
        nwd = form.search.data
        return redirect('/search/{}/1'.format(nwd))

    pagination = Post(publish=1).set_pagination(page, 20).select(oderby='timestamp', isasc=False)
    return render_template('/main/post.html',
                           form=form,
                           pagination=pagination)


@main.route('/post/<time>/<id>', methods=['GET', 'POST'])
def postPage(time, id):
    page = request.args.get('page', 1, type=int)
    post = Post(id=id).select(getone=True)
    pagination = Comment(operand_id=post.id).set_pagination(page=page, paging=20).select(oderby='timestamp', isasc=False)
    form = SearchForm()
    comment_form = CommentForm()
    is_thumb = None
    is_collect = None
    if not post.publish:
        abort(404)
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))
    if current_user.can(Permission.WRITE):
        is_thumb = post.is_thumb(current_user.id)
        is_collect = post.is_collect(current_user.id)
        post.browse_it()
    if current_user.can(Permission.WRITE) and comment_form.validate_on_submit():
        post.set_comment(body=comment_form.body.data, user_id=current_user.id)
        return redirect(post.path + '#post')

    for comment in pagination.items:
        comment.info = Info(id=comment.user_id).select(getone=True)

    return render_template('/postbase.html',
                           operand=post,
                           form=form,
                           comment_form=comment_form,
                           pagination=pagination,
                           url=post.path,
                           isThumb=is_thumb,
                           isCollect=is_collect)


@main.route('/page/<type>/<time>/<filename>', methods=['GET', 'POST'])
def staticPage(type, time, filename):
    page = request.args.get('page', 1, type=int)
    url = '/page/{}/{}/{}'.format(type, time, filename)
    news = News(filename=filename).select(getone=True)
    pagination = Comment(operand_id=news.id).set_pagination(page=page, paging=20).select(oderby='timestamp',isasc=False)
    form = SearchForm()
    comment_form = CommentForm()
    is_thumb = None
    is_collect = None
    if not news.id:
        abort(404)
    if form.validate_on_submit():
        wd = form.search.data
        return redirect('/search/{}/1'.format(wd))
    if current_user.can(Permission.WRITE):
        is_thumb = news.is_thumb(current_user.id)
        is_collect = news.is_collect(current_user.id)
        news.browse_it(current_user.id)
    if current_user.can(Permission.WRITE) and comment_form.validate_on_submit():
        news.set_comment(body=comment_form.body.data, user_id=current_user.id)
        return redirect(url + '#post')

    with open('info/time/{}.json'.format(time), 'r', encoding='utf-8') as f:
        timeDict = json.loads(f.read())
    with open('info/type/{}.json'.format(type), 'r', encoding='utf-8') as f:
        typeDict = json.loads(f.read())
    timeList = []
    timeLen = len(timeDict)
    typeList = []
    typeLen = len(typeDict)
    for i in range(10):
        if i < timeLen:
            timeList.append(timeDict[str(i)])
        if i < typeLen:
            typeList.append(typeDict[str(i)])

    for comment in pagination.items:
        comment.info = Info(id=comment.user_id).select(getone=True)

    return render_template(url,
                           operand=news,
                           timeList=timeList,
                           typeList=typeList,
                           time=time,
                           type=type,
                           form=form,
                           comment_form=comment_form,
                           pagination=pagination,
                           isThumb=is_thumb,
                           isCollect=is_collect,
                           url=url)


@main.route('/user/<username>')
def user_show(username):
    user = Account(account=username).select(getone=True)
    if user.id is None:
        abort(404)
    follows = user.get_follow()
    followers = user.get_follower()
    historys = History(user_id=user.id).select(oderby='timestamp', isasc=False)
    if current_user.can(Permission.WRITE):
        user.browse_it(current_user.id)
    return render_template('user/user_show.html', user=user, historys=historys,
                           follows=follows, followers=followers)


@main.route('/user/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    info = Info(id=current_user.id)
    info.select(getone=True)
    if form.validate_on_submit():
        info.realname = check(form.realname.data)
        info.about_me = check(form.about_me.data)
        info.phone = check(form.phone.data)
        info.birthday = check(form.birthday.data)
        info.hometown = check(form.hometown.data)
        info.location = check(form.location.data)
        info.job = check(form.job.data)
        info.company = check(form.company.data)
        info.school = check(form.school.data)
        info.update()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user_show', username=current_user.account))

    form.realname.data = check(info.realname)
    form.about_me.data = check(info.about_me)
    form.phone.data = check(info.phone)
    if info.sex is '男':
        sex = 0
    else:
        sex = 1
    form.sex.data = check(sex)
    form.birthday.data = info.birthday
    form.hometown.data = check(info.hometown)
    form.location.data = check(info.location)
    form.job.data = check(info.job)
    form.company.data = check(info.company)
    form.school.data = check(info.school)
    return render_template('user/user_edit.html', form=form)


def check(vattr):
    if vattr:
        if isinstance(vattr, str) or isinstance(vattr, int):
            return vattr
        else:
            return str(vattr)
    else:
        return ''


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    account = Account()
    account.id = id
    account.select(getone=True)
    if not account.account:
        abort(404)
    info = Info()
    info.id = account.info_id
    info.select(getone=True)
    form = EditProfileAdminForm(account=account)
    if form.validate_on_submit():
        account.account = check(form.username.data)
        account.confirmed = check(form.confirmed.data)
        account.role_id = check(account.role.data)
        account.update()
        info.realname = check(form.realname.data)
        info.about_me = check(form.about_me.data)
        info.phone = check(form.phone.data)
        info.birthday = check(form.birthday.data)
        info.hometown = check(form.hometown.data)
        info.location = check(form.location.data)
        info.job = check(form.job.data)
        info.company = check(form.company.data)
        info.school = check(form.school.data)
        info.update()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=account.account))

    form.email.data = account.email
    form.username.data = account.account
    form.confirmed.data = bool(account.confirmed)
    form.role.data = account.role_id

    form.realname.data = check(info.realname)
    form.about_me.data = check(info.about_me)
    form.phone.data = check(info.phone)
    form.sex.data = check(info.sex)
    form.birthday.data = check(info.birthday)
    form.hometown.data = check(info.hometown)
    form.location.data = check(info.location)
    form.job.data = check(info.job)
    form.company.data = check(info.company)
    form.school.data = check(info.school)
    return render_template('user/user_edit.html', form=form, info=info)

