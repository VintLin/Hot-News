from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from Model.model import Account


class LoginForm(FlaskForm):
    email = StringField('Email : ', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码 : ', validators=[DataRequired()])
    remember_me = BooleanField('保存信息')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('Email : ', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('账号 : ', validators=[DataRequired(), Length(1, 64),
                                                Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名必须以字母开头,'
                                                                                      '之后可以填写数字、字母、下划线、点.')])
    password = PasswordField('密码 : ', validators=[DataRequired(), EqualTo('password2', message='密码不对应.')])
    password2 = PasswordField('确认密码 : ', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        account = Account()
        account.email = field.data
        account.select(getone=True)
        if account.id is not None:
            raise ValidationError('Email已经存在.')

    def validate_username(self, field):
        account = Account()
        account.account = field.data
        account.select(getone=True)
        if account.id is not None:
            raise ValidationError('账户已经存在.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧的密码 : ', validators=[DataRequired()])
    password = PasswordField('新的密码 : ', validators=[
        DataRequired(), EqualTo('password2', message='密码不对应.')])
    password2 = PasswordField('确认密码 : ', validators=[DataRequired()])
    submit = SubmitField('更改密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('输入您的Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('重设密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新的密码 : ', validators=[DataRequired(),
                                                    EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认密码 : ', validators=[DataRequired()])
    submit = SubmitField('重设密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('新的Email : ', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码 : ', validators=[DataRequired()])
    submit = SubmitField('重设Email')

    def validate_email(self, field):
        account = Account()
        account.email = field.data
        account.select(getone=True)
        if account.id is not None:
            raise ValidationError('Email已经存在.')


class PostForm(FlaskForm):
    TYPE = {'0': '生活', '1': '新闻', '2': '居家', '3': '旅游', '4': '学习', '5': '感悟'}
    INDEX = {'生活': '0', '新闻': '1', '居家': '2', '旅游': '3', '学习': '4', '感悟': '5'}
    title = StringField('标题:', validators=[DataRequired(), Length(1, 64)])
    body = PageDownField("正文内容 : ",  validators=[DataRequired()])
    type = SelectField('文章类型 : ', coerce=str)
    publish = SubmitField('发 布')
    save = SubmitField('保 存')

    def __init__(self):
        super(PostForm, self).__init__()
        self.type.choices = [('0', '生活'),
                            ('1', '新闻'),
                            ('2', '居家'),
                            ('3', '旅游'),
                            ('4', '学习'),
                            ('5', '感悟')]