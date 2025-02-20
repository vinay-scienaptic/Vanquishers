

import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_MAIL = True
MAIL_USER = os.environ.get("mail_agent")
MAIL_USER_PASSWORD = os.environ.get("mail_agent_password")
# MAIL_FROM = os.environ.get("mail_from")
# MAIL_TO = str(os.environ.get("mail_to")).splitlines()
# MAIL_CC = str(os.environ.get("mail_cc")).splitlines()

MAIL_FROM = "vinay.pottabathini@scienaptic.com"
MAIL_TO = "vinay040998@gmail.com"
MAIL_CC = ""

def send_alert():
    """to send alert

    Args:
        data (_type_): _description_
    """
    multipart_message = MIMEMultipart()
    multipart_message["From"] = MAIL_FROM
    multipart_message["To"] = ", ".join(MAIL_TO)
    multipart_message["Cc"] = ", ".join(MAIL_CC)
    multipart_message["Subject"] = "Client Request"
    msg = "Hello THis is email text"
    multipart_message.attach(MIMEText(msg, "html"))
    smtplib_server = smtplib.SMTP(host="smtp.gmail.com", port=587)
    smtplib_server.starttls()
    smtplib_server.login(str(MAIL_USER), str(MAIL_USER_PASSWORD))
    smtplib_server.send_message(multipart_message)
    smtplib_server.quit()
