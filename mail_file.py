import re
import smtplib

#subjuct import module
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from trainemail import TrackImages


#attachment import module
from email.mime.base import MIMEBase
from email import encoders

#subject starts
email_user = 'girik7411@gmail.com'
email_send = 'girikumar.kolla@gmail.com'
subject = 'Python!'

msg = MIMEMultipart()
msg['From'] = email_user
msg['To'] = email_send
msg['subject'] = subject

body = "hello sir"
msg.attach(MIMEText(body,'plain'))

# attachment starts

filename = attendance
attachment = open(filename, 'rb')

part = MIMEBase("application","octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header("content-Disposition","attachment;filename = %s" %filename)

msg.attach(part)
# attachment ends
text = msg.as_string()
#subject ends
server = smtplib.SMTP('smtp.gmail.com',587)

server.starttls()
# login 
server.login(email_user,'Kumari96')
#sending mail
server.sendmail(email_user,email_send,text)

server.close()
