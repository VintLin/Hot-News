# -*- coding: UTF-8 -*-

from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr


def _format_addr(name, addr):
    return formataddr((Header(name, 'utf-8').encode(), addr))


def sendEmail(to_addr, url, name='用户'):
    from_addr = 'voterlin@foxmail.com'
    password = 'iglxwajzbjzxbaaj'
    smtp_server = 'smtp.qq.com'
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    subject = 'HotNews:账号注册验证'
    mail_msg = '''
    <h3>
    <p>亲爱的 {} :</p>
    <p>为了激活您的账号请点击下面的连接</p>
    <p><a href="{}">点击此链接完成认证</a></p>
    <p>感谢您的加入</p>
    <p>HotNews</p>
    </h3>
    '''.format(name, url)

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = _format_addr('HotNews', from_addr)
    message['To'] = _format_addr('我', to_addr)
    message['Subject'] = Header(subject, 'utf-8').encode()
    try:
        server = SMTP_SSL(smtp_server)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], message.as_string())
        server.quit()
        return True
    except:
        return False
