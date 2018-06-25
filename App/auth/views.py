from flask import render_template, redirect, request, url_for, flash, session, abort
from flask_login import login_user, login_required, logout_user, current_user
from .forms import *
from model.model import *
from . import auth
from App.tool.sendEmail import sendEmail


@auth.route('/Login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        account = Account(email=form.email.data).select(getone=True)
        if account.password_hash is not None and account.verify_password(form.password.data):
            login_user(account, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('账号或密码输入错误.')
    return render_template('auth/login.html', form=form)


@auth.route('/user')
@login_required
def user():
    comments = Comment(user_id=current_user.id).select(limit=50, oderby='timestamp', isasc=False)
    thumbs = Thumb(user_id=current_user.id).select(limit=50, oderby='timestamp', isasc=False)
    collects = Collect(user_id=current_user.id).select(limit=50, oderby='timestamp', isasc=False)
    historys = History(user_id=current_user.id).select(limit=50, oderby='timestamp', isasc=False)
    for comment in comments:
        comment.item = OPERAND[comment.operand](id=comment.operand_id).select(getone=True)
    for thumb in thumbs:
        thumb.item = OPERAND[thumb.operand](id=thumb.operand_id).select(getone=True)
    for collect in collects:
        print(collect.user_id, collect.operand, collect.operand_id, collect.timestamp)
        collect.item = OPERAND[collect.operand](id=collect.operand_id).select(getone=True)
    return render_template('user/user.html', comments=comments, thumbs=thumbs, collects=collects, historys=historys)


@auth.route('/user-info')
@login_required
def user_info():
    info = Info(id=current_user.id).select(getone=True)
    if info.name is None:
        abort(404)
    return render_template('user/user_info.html', info=info)


@auth.route('/user-follow')
@login_required
def user_follow():
    f = request.args.get('f', 0, type=int)
    if f:
        users = current_user.get_follow()
    else:
        users = current_user.get_follower()
    return render_template('user/user_follow.html', users=users)


@auth.route('/user-post', methods=['GET'])
@login_required
def user_post():
    isdelete = request.args.get('delete', 0, type=int)
    user_id = request.args.get('user_id', 0, type=int)
    post_id = request.args.get('post_id', 0, type=int)
    if isdelete and post_id and user_id is current_user.id:
        Post(user_id=user_id, id=post_id).delete()
    post_save = Post(user_id=current_user.id, publish=False).select(oderby='timestamp', isasc=False)
    post_publish = Post(user_id=current_user.id, publish=True).select(oderby='timestamp', isasc=False)
    return render_template('user/user_post.html', post_publish=post_publish, post_save=post_save)


@auth.route('/post_edit', methods=['GET', 'POST'])
@login_required
def post_edit():
    # 0 new post /1 edit old post
    type = request.args.get('type', 0, type=int)
    form = PostForm()
    post = Post(user_id=current_user.id)

    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.type = form.TYPE[form.type.data]
        post.publish = post.publish or '发 布' in request.form.values()
        if type is 0:
            post.insert()
        elif type is 1:
            post.id = request.args.get('post_id', 0, type=int)
            post.update()
        return redirect('auth/user-post')

    if type is 1:
        post_id = request.args.get('post_id', 0, type=int)
        post = Post(id=post_id).select(getone=True)
        form.title.data = post.title
        form.body.data = post.body
        form.type.data = form.INDEX[post.type]
    return render_template('user/post_edit.html', form=form)


@auth.route('/Logout')
@login_required
def logout():
    logout_user()
    flash('你已经退出登入.')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('您的账户已经得到认证. 谢谢!')
    else:
        flash('认证链接已经过期, 请重新认证.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    sendEmail(current_user.email, url_for('auth.confirm', token=token, _external=True), current_user.account)
    flash('新的验证邮件已经发送到您的邮箱了.')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        account = Account(email=form.email.data, account=form.username.data)
        account.password = form.password.data
        account.insert()
        flash('注册成功! 你现在可以登入.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        account = Account(email=form.email.data).select(getone=True)
        if account.id:
            token = account.generate_reset_token()
            sendEmail(account.email, url_for('auth.password_reset', token=token, _external=True), account.account)
            flash('一封邮件已经发入您的新邮箱,请及时确认.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if Account.reset_password(token, form.password.data):
            flash('您的密码已经更新.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/edit_account/<oper>', methods=['GET', 'POST'])
@login_required
def edit_account(oper):
    isEmail = oper == 'eml'
    if isEmail:
        form = ChangeEmailForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.password.data):
                new_email = form.email.data
                token = current_user.generate_email_change_token(new_email)
                sendEmail(current_user.email, url_for('auth.change_email', token=token, _external=True),
                          current_user.account)
                flash('为了确认这是您的邮箱,一封邮件已经发入您的新邮箱,请及时确认.')
                return redirect(url_for('main.index'))
            else:
                flash('Email或密码错误.')
    else:
        form = ChangePasswordForm()
        if form.validate_on_submit():
            if current_user.verify_password(form.old_password.data):
                current_user.password = form.password.data
                current_user.update()
                flash('您的密码已经重置')
                return redirect(url_for('main.index'))
            else:
                flash('密码错误.')
    return render_template("auth/edit_account.html", form=form, isEmail=isEmail)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('您的Email地址已经更新.')
    else:
        flash('请求以过期.')
    return redirect(url_for('main.index'))
