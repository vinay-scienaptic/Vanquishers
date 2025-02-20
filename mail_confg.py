

import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SEND_MAIL = True
# MAIL_USER = os.environ.get("mail_agent")
# MAIL_USER_PASSWORD = os.environ.get("mail_agent_password")

MAIL_USER = "techsupport@scienaptic.com"
MAIL_USER_PASSWORD = "ojltbktqfpneztep"



# MAIL_FROM = os.environ.get("mail_from")
# MAIL_TO = str(os.environ.get("mail_to")).splitlines()
# MAIL_CC = str(os.environ.get("mail_cc")).splitlines()

MAIL_FROM = "techsupport@scienaptic.com"
MAIL_TO = "vinay.pottabathini@scienaptic.com"
MAIL_CC = ""

# def send_alert():
#     """to send alert

#     Args:
#         data (_type_): _description_
#     """
#     multipart_message = MIMEMultipart()
#     multipart_message["From"] = MAIL_FROM
#     multipart_message["To"] = ", ".join(MAIL_TO)
#     multipart_message["Cc"] = ", ".join(MAIL_CC)
#     multipart_message["Subject"] = "Client Request"
#     msg = "Hello THis is email text"
#     multipart_message.attach(MIMEText(msg, "html"))
#     smtplib_server = smtplib.SMTP(host="smtp.gmail.com", port=587)
#     smtplib_server.starttls()
#     smtplib_server.login(str(MAIL_USER), str(MAIL_USER_PASSWORD))
#     smtplib_server.send_message(multipart_message)
#     smtplib_server.quit()




import smtplib
from email.message import EmailMessage

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "techsupport@scienaptic.com"
EMAIL_PASSWORD = "ojltbktqfpneztep"

def send_alert():
    msg = EmailMessage()
    msg["Subject"] = "Test Email"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = "srikanth.k@scienaptic.com"
    msg.set_content("This is a test email.")

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Authenticate
        server.send_message(msg)  # Send email
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")