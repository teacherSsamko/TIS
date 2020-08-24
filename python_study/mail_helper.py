import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid

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


def send_html_mail():
    smtp = smtplib.SMTP(host=pikavue['host'], port=pikavue['port'])
    smtp.starttls()
    smtp.ehlo()
    smtp.login(pikavue['auth']['user'],pikavue['auth']['pass'])

    msg = EmailMessage()
    msg['Subject'] = 'HTML test'
    msg['To'] = 'ssamko@gdflab.com'
    msg['From'] = pikavue['auth']['user']
    msg.set_content("""\
        Sorry.. your item was failed to upscale for some reason

        Possible reasons below
        - Lack of server resouce. we operate this server with minimum spec for serving our service free.
        - Video running time is too long to upscale it. Depending video quality, possible running time of video is diffent on this server.
        - Some bugs that we should fix it. We are developing our technology.

        Team pikaVue
        """)
    msg.add_alternative("""\
        <html>
        <head></head>
        <body style"line-height:150%; font-family: arial; font-size:14px; color: #000000;">
		<h1>Upscale Failed..</h1> 
		<h3>Sorry.. your item was failed to upscale for some reason</h3>
		<h3>Possible reasons below</h3>
		<ul>
            <li>Lack of server resouce. we operate this server with minimum spec for serving our service free. </li>
            <li>Video running time is too long to upscale it. Depending video quality, possible running time of video is diffent on this server.</li>
            <li>Some bugs that we should fix it. We are developing our technology.</li>
        </ul>
		<p>Team pikaVue :)</p>
		</body></html>
        """, subtype='html')
    # smtp.sendmail(from_addr=pikavue['auth']['user'], to_addrs='ssamko@gdflab.com', msg=msg.as_string())
    smtp.send_message(msg)

    smtp.quit()
    print("mail sent")