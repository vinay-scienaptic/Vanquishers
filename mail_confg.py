

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

def to_techsupport_mail(data):
    msg = EmailMessage()
    msg["Subject"] = "Demo Requested by Customer"
    email_body = f"Hi Techsupport, User named {data['recipient_name']} has requested for a Demo. Please schedule a call. Thank You!"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(email_body)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Authenticate
        server.send_message(msg)  # Send email
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    return None



def to_recipient_mail(data):
    msg = EmailMessage()
    msg["Subject"] = "ScienapticAI Received Your Request"

    email_body = f'Hi {data["recipient_name"]} we have received your request for Demo on {data["recipient_date"]}. Our Techsupport will contact you soon. Thanks for reaching out to Scienaptic.'
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = data['recipient_email']
    
    msg.set_content(email_body)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Authenticate
        server.send_message(msg)  # Send email
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
    return None