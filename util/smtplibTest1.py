#coding: utf-8
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

sender = '18770917652@163.com'
receiver = '326831169@qq.com'
smtpserver = 'smtp.163.com'
username = '18770917652@163.com'
password = '4017aibeibei'

#邮件标题
subject = '邮件标题'

#邮件内容(文本格式)
html='邮件内容qwerqwfadeqerqwerqweqwerqwer'
msg = MIMEText(html)
msg['Subject'] = Header(subject, 'utf-8' )
msg['from'] = '18770917652@163.com'
msg['to'] = '326831169@qq.com'

# 构造图片链接
sendimagefile = open(r'D:\pythontest\testimage.png', 'rb').read()
image = MIMEImage(sendimagefile)
image.add_header('Content-ID', '<image1>')
image["Content-Disposition"] = 'attachment; filename="testimage.png"'
msg.attach(image)

smtp = smtplib.SMTP()
smtp.connect( smtpserver )
smtp.login( username, password )
smtp.sendmail( sender, receiver, msg.as_string())
smtp.quit()