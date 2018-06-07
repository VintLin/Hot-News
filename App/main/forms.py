from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError

from Model.model import Role, Account


class SearchForm(FlaskForm):
    search = StringField('Search...', validators=[DataRequired()])
    submit = SubmitField('搜索')


class EditProfileForm(FlaskForm):
    realname = StringField('真实姓名 : ', validators=[Length(0, 40)])
    about_me = TextAreaField('个人简介 : ')
    phone = StringField('电话 : ', validators=[Length(0, 20)])
    sex = SelectField('性别 : ', coerce=str, choices=[('0', '男'), ('1', '女')])
    birthday = DateField('出生日期 : ')
    hometown = StringField('故乡 : ', validators=[Length(0, 64)])
    location = StringField('所在地 : ', validators=[Length(0, 64)])
    job = StringField('职业 : ', validators=[Length(0, 64)])
    company = StringField('公司 : ', validators=[Length(0, 64)])
    school = StringField('学校 : ', validators=[Length(0, 64)])
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email : ', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('昵称 : ', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '昵称只能输入字母、下划线、点.')])
    # role
    confirmed = BooleanField('认证 : ')
    role = SelectField('权限 : ', coerce=int)
    # info
    realname = StringField('真实姓名 : ', validators=[Length(0, 64)])
    about_me = TextAreaField('个人简介 : ')
    phone = StringField('电话 : ', validators=[Length(0, 64)])
    sex = SelectField('性别 : ', coerce=str)
    birthday = DateField('出生日期 : ')
    hometown = StringField('故乡 : ', validators=[Length(0, 64)])
    location = StringField('所在地 : ', validators=[Length(0, 64)])
    job = StringField('职业 : ', validators=[Length(0, 64)])
    company = StringField('公司 : ', validators=[Length(0, 64)])
    school = StringField('学校 : ', validators=[Length(0, 64)])
    submit = SubmitField('提交')

    def __init__(self, account, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        role = Role()
        self.sex.choices = [('0', '男'), ('1', '女')]
        self.role.choices = [(role.id, role.name) for role in role.select(oderby='name')]
        self.account = account

    def validate_email(self, field):
        account = Account(email=field.data).select(getone=True)
        if field.data != self.account.email and account.id:
            raise ValidationError('Email已经注册.')

    def validate_username(self, field):
        account = Account(account=field.data).select(getone=True)
        if field.data != self.account.username and account.id:
            raise ValidationError('用户名已经使用.')


class CommentForm(FlaskForm):
    body = TextAreaField("说出你的想法 : ", validators=[DataRequired()])
    submit = SubmitField('发表评论')


class ThumbButton(FlaskForm):
    submit = SubmitField()


class Button(FlaskForm):
    submit = SubmitField()