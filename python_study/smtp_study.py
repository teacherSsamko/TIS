import smtplib
from email.mime.text import MIMEText

def sendMail(me, you, msg):
    smtp = smtplib.SMTP('smtp.pikavue.com', 7409)
    smtp.login("hello@smtp.pikavue.com", 'gdfnas!@#')
    msg = MIMEText(msg)
    msg['Subject'] = 'TEST'
    smtp.sendmail(me, you, msg.as_string())
    smtp.quit()

# sendMail('hello@smtp.pikavue.com', 'ssamko@gdflab.com', 'TEXT')
try:
    smtp = smtplib.SMTP('smtp.pikavue.com', 7409)
    smtp.ehlo()
    smtp.starttls()
    smtp.login("hello@smtp.pikavue.com","gdfnas!@#")

    msg = MIMEText('hello pikavue')
    msg['Subject'] = 'Test'
    msg['To'] = 'ssamko@kakao.com'
    smtp.sendmail('hello@smtp.pikavue.com', 'ssamko@kakao.com', msg.as_string())

    smtp.quit()
except:
    print("Error")

'''
"smtp": {
        "service": "pikavue",
        "secureConnection": true,
        "host": "smtp.pikavue.com",
        "port": 7409,
        "secure": false,
        "auth": {
            "user": "hello@smtp.pikavue.com",
            "pass": "gdfnas!@#"
        },
        "tls":{
            "rejectUnauthorized": false
        }
    }
'''