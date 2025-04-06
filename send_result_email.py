import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")


def manipulate_gpt_output_to_scaffold_email(gpt_output):
    groups = gpt_output.split("{}")
    if len(groups) == 0:
        return gpt_output

    emails = groups[0].split("[]")

    html_blocks_for_output = []

    for group, idx in groups[1:]:
        html_blocks_for_output.append(
            f"""<p>{group}</p><br><button><a href="mailto:{emails[idx].strip()}">\
                    Send Intro</a></button><p>*Note: this will not send an email\
                    until you make changes and confirm</p><br><br>"""
        )

    final_html_email = """"""
    for html_block in html_blocks_for_output:
        final_html_email = f"""{final_html_email}{html_block}"""

    print(final_html_email)
    return final_html_email


def send_email(recipient_email, gpt_output):
    msg = MIMEMultipart("alternative")
    msg["From"] = "Automeet"
    msg["To"] = recipient_email
    msg["Subject"] = "Automated output from Automeet"

    msg.attach(MIMEText(f"""{gpt_output}""", "plain"))
    msg.attach(
        MIMEText(f"""{manipulate_gpt_output_to_scaffold_email(gpt_output)}""", "html")
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.send_message(msg)
