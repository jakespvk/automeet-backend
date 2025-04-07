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

    for idx, group in enumerate(groups[1:]):
        # email_intro_text = group[
        #     group.index("Potential email introduction text:") : group.index("<")
        # ].strip()
        # print(email_intro_text)
        html_blocks_for_output.append(
            f"""{group}<br><a href="mailto:?to={emails[idx].strip()}\
                    &subject=Introduction&body=Hey [names]">\
                    Send Intro</a><p>*Note: this will not send an email\
                    until you make changes and confirm</p><br><br>"""
        )

    final_html_email = """"""
    for html_block in html_blocks_for_output:
        final_html_email = f"""{final_html_email}{html_block}"""

    final_html_email = (
        """\
        <html>
            <head>
                <meta name="color-scheme" content="light dark">
                <meta name="supported-color-schemes" content="light dark">
            </head>
            <style>
                @media (prefers-color-scheme: dark) {
                    a {
                        background-color: white;
                        color: black;
                    }
                }
                @media (prefers-color-scheme: light) {
                    a {
                        background-color: black;
                        color: white;
                    }
                }
            </style>
            <body> 
                <h1 style="font-size:2rem;">Automeet</h1>
                """
        + final_html_email
        + """
            </body>
        </html>
    """
    )

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
        s.sendmail("Automeet", recipient_email, msg.as_string())
