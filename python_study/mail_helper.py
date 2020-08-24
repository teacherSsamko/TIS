import os
import sys
import smtplib
from email.mime.text import MIMEText

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import private.config


pikavue = private.config.PIKAVUE_SMTP

smtp = smtplib.SMTP(host=pikavue['host'], port=pikavue['port'])

def send_mail(mail_to, body, subject='test'):
    smtp = smtplib.SMTP(host=pikavue['host'], port=pikavue['port'])
    smtp.starttls()
    smtp.ehlo()
    smtp.login(pikavue['auth']['user'],pikavue['auth']['pass'])

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = mail_to
    msg['From'] = pikavue['auth']['user']
    smtp.sendmail(from_addr=pikavue['auth']['user'], to_addrs='ssamko@gdflab.com', msg=msg.as_string())

    smtp.quit()
    print("mail sent")