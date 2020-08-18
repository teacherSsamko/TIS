import os
import sys
import smtplib
from email.mime.text import MIMEText

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import private.config

kakao = private.config.KAKAO_SMTP
pikavue = private.config.PIKAVUE_SMTP

smtp = smtplib.SMTP(host=pikavue['host'], port=pikavue['port'])
# smtp = smtplib.SMTP_SSL(host=kakao['host'], port=kakao['port'])
smtp.starttls()
smtp.ehlo()
smtp.login(pikavue['auth']['user'],pikavue['auth']['pass'])

msg = MIMEText('hello pikavue')
msg['Subject'] = 'Test'
msg['To'] = 'ssamko@gdflab.com'
msg['From'] = pikavue['auth']['user']
smtp.sendmail(from_addr=pikavue['auth']['user'], to_addrs='ssamko@gdflab.com', msg=msg.as_string())
# smtp.sendmail(from_addr=kakao['mail'], to_addrs='ssamko@gdflab.com', msg=msg.as_string())


smtp.quit()
print("mail sent")

"""
KAKAO_SMTP = {
    "id":'id',
    "mail":"id@kakao.com",
    "password":"password",
    "host":"smtp.kakao.com",
    "port":465
}
"""
