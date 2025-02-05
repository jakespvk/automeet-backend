def handle_login(user_email):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import os
    from dotenv import load_dotenv, dotenv_values
    from jose import jwt

    load_dotenv()

    gmail_user = os.getenv("gmail_user")
    gmail_password = os.getenv("gmail_password")

    msg = MIMEText(f"Click this link to login: {link}")
    msg["Subject"] = "Your Requested Login Link"
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    login_link = "12345"
    html = f'<html><h1>Automeet</h1><a href="http://localhost:8000/verify?token={login_link}">Login</a></html>'
    email_text = MIMEText(html, "html")
    msg.attach(email_text)

    smtpserver = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtpserver.ehlo()
    smtpserver.login(gmail_user, gmail_password)

    sent_from = gmail_user
    sent_to = sent_from
    login_link = "12345"
    email_text = f'<html><h1>Automeet</h1><a href="http://localhost:8000/verify?token={login_link}">Login</a></html>'
    smtpserver.send_message(msg)

    smtpserver.close()

    return login_link
