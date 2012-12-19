#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import re

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os


url = 'http://www.char4.com'
html = urllib2.urlopen(url).read()
html2 = BeautifulSoup(html)

final = "";

for html3 in html2.findAll('form'):
    html4 = html3.find('input', {'name':'domain'})
    html5 = html4.get('value')
    if re.match(r'^[a-z]*$',html5):
        final = final + html5 + "\n"

print final

gmail_user = "me@gmail.com"
gmail_pwd = "mypass"

def mail(to, subject, text, attach=None):
    msg = MIMEMultipart()
    
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(text))
    
    if attach:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)
    
    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()
    
mail("aaronr@z-pulley.com",
     "new 4 char domains available",
     final)

    
