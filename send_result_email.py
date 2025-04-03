from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import os

load_dotenv()

gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")


def send_email(recipient_email, gpt_output):
    msg = EmailMessage()
    msg["From"] = "Automeet"
    msg["To"] = recipient_email
    msg["Subject"] = "Automated output from Automeet"
    msg.set_content(gpt_output)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.send_message(msg)
