#!/usr/bin/env python
#-*-coding:utf8-*-

import os, sys, smtplib, mimetypes
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

MAIL_LIST = ["test@qq.cn"]
MAIL_HOST = "localhost"
MAIL_USER = "qq@qq.cn"
MAIL_PASS = "123456"
MAIL_POSTFIX = "123456"
MAIL_FROM = MAIL_USER + "<"+MAIL_USER + ">"

def send_mail(subject, content, filename=None, filepath = None):
    try:
        if filepath == None or os.path.exists(filepath) == False:
            return False
        message = MIMEMultipart()
        message.attach(MIMEText(content, _charset="UTF-8"))
        message['Subject'] = Header(subject, "utf-8")
        message["From"] = MAIL_FROM
        message["To"] = ";".join(MAIL_LIST)
        if filepath != None and os.path.exists(filepath):
            ctype, encoding = mimetypes.guess_type(filepath)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(filepath, "rb"))[0], _subtype = subtype)
                attachment.add_header("Content-Disposition", "attachment", filename = filename)
                message.attach(attachment)

        smtp = smtplib.SMTP_SSL(MAIL_HOST,994)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(MAIL_USER, MAIL_PASS)
        smtp.sendmail(MAIL_FROM, MAIL_LIST, message.as_string())
        smtp.quit()

        return True
    except Exception, errmsg:
        print "Send mail failed to: %s" % errmsg

    return False

if __name__ == "__main__":
    if len(sys.argv)!=4:
        print "error argv"
        sys.exit(0)
    idate = sys.argv[1]
    content = sys.argv[2]
    yy = sys.argv[3]
    print '%s,%s,%s' % (idate, content, appkey)
    if send_mail("JS CT alias new - %s" % idate, "Hi all, test\r\n%s" % (idate,content), "%s-alias_new.%s" % (appkey,idate), r"/opt/data/%s-new.%s" % (yy, idate)):
        print "发送成功！"
    else:
        print "发送失败！"
    if send_mail("JS CT alias online - %s" % idate, "Hi all, test\r\n%s" % (idate,content), "%s-alias_ol.%s" % (appkey, idate), r"/opt/data/%s-ol.%s" % (yy,idate)):
        print "发送成功！"
    else:
        print "发送失败！"
