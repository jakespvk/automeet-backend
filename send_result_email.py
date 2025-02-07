from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")


def send_email(recipient_email, gpt_output):
    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)

    sent_from = "Automeet"
    sent_to = recipient_email
    email_text = (
        "Hello, this is an automated email from Automeet. Here is the data:"
        + gpt_output
    )
    smtpserver.sendmail(sent_from, sent_to, email_text)

    smtpserver.close()
