import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEText


load_dotenv()

gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")


def manipulate_gpt_output_to_scaffold_email(gpt_output):
    groups = gpt_output.split("{}")

    html_blocks_for_output = []

    for group in groups:
        html_blocks_for_output.append(
            f"""<p>{group}</p><br><button><a href="mailto:jakespvk@gmail.com">\
                    Send Intro</a></button><br><br>"""
        )

    final_html_email = """"""
    for html_block in html_blocks_for_output:
        final_html_email = f"""{final_html_email}{html_block}"""


def send_email(recipient_email, gpt_output):
    msg = MIMEMultipart("alternative")
    msg["From"] = "Automeet"
    msg["To"] = recipient_email
    msg["Subject"] = "Automated output from Automeet"

    msg.attach(MIMEText(f"""{gpt_output}"""), "plain")
    msg.attach(
        MIMEText(f"""{manipulate_gpt_output_to_scaffold_email(gpt_output)}"""), "html"
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.send_message(msg)
