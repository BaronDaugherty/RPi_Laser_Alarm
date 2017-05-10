#@author: Baron Daugherty
#mailer.py
#you really shouldn't use this... it's 100% insecure. I'll get to replacing it someday... maybe.
#mailer can be imported and used for its mail functions
#or as a standalone script for mail with attachments
#uses GMAIL but you can modify mailServer variable below to support whatever service you choose

#imports
import smtplib
import os
import sys 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

#mail including attachments 
def mail(gmail_user, gmail_pwd, to, subject, text, files):
	msg = MIMEMultipart()
 
   	msg['From'] = gmail_user
   	msg['To'] = to
   	msg['Subject'] = subject

   	msg.attach(MIMEText(text))
 
	#files is a list of file paths
   	for f in files:
   		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(f,"rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
		msg.attach(part)

	send(gmail_user, gmail_pwd, to, msg)

#plain text mail
def mail(gmail_user, gmail_pwd, to, subject, text):
	msg = MIMEMultipart()

	msg['From'] = gmail_user
	msg['To'] = to
	msg['Subject'] = subject

	msg.attach(MIMEText(text))
	send(gmail_user, gmail_pwd, to, msg)

#send the mail
def send(gmail_user, gmail_pwd, to, msg):
	mailServer = smtplib.SMTP("smtp.gmail.com", 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(gmail_user, gmail_pwd)
	mailServer.sendmail(gmail_user, to, msg.as_string())
	mailServer.close()

#in case you want to run it as a standalone program(assumes attachments)
def main():
	mail(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

main()
