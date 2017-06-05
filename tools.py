#coding=utf-8
from flask_mail import Message
from api import mail
from api import app


def send_email(recipients):
    subject = u"感谢您申领测试机,请填写附件表一并签字,交至市场部肖翔处"
    msg = Message(subject, sender=(u"肖翔","xiaoxiang@migu.cn"),recipients=recipients)
    msg.body = u"感谢您申领测试机,请填写附件表一并签字,交至市场部肖翔处"
    with app.open_resource(u"regulations.pdf") as fp:
        msg.attach(filename=u"regulations.pdf", content_type="application/pdf",data= fp.read(),disposition='Content-Disposition')
    mail.send(msg)