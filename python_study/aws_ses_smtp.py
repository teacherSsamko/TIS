from smtplib import SMTP

with SMTP("email-smtp.us-west-2.amazonaws.com") as smtp:
    smtp.noop()