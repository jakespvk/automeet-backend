import sqlite3

# from typing import Annotated
# from doing_stuff.db_providers.active_campaign_adapter import (
#     get_activecampaign_connection,
#     get_activecampaign_data,
# )
from doing_stuff.db_providers.sqlite_adapter import get_data
from doing_stuff.query_gpt import chat_with_gpt
from doing_stuff.send_result_email import send_email

import threading
import schedule

from jose import jwt, JWTError
import secrets

from fastapi import FastAPI, HTTPException, Query  # Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from datetime import datetime, timedelta

import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv  # , dotenv_values

load_dotenv()


gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")

SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 1


class EmailRequest(BaseModel):
    email: EmailStr


class User:
    email: str
    subscription: bool
    db_type: str
    columns: list
    column_limit: int
    row_limit: int
    login_token: str

    def __init__(
        self,
        email,
        subscription,
        db_type,
        columns,
        column_limit,
        row_limit,
        login_token,
    ):
        self.email = email
        self.subscription = subscription
        self.db_type = db_type
        self.columns = columns
        self.column_limit = column_limit
        self.row_limit = row_limit
        self.login_token = login_token


def create_magic_link_token(email: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expiration}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def send_magic_link(email: str, token: str):
    magic_link = f"http://localhost:3000/magic?token={token}"
    msg = MIMEText(f"Click this link to log in: {magic_link}")
    msg["Subject"] = "Your magic link login"
    msg["From"] = "Automeet"
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.send_message(msg)


def get_user(user_email):
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (user_email,),
    )
    user = cursor.fetchone()
    print(user)
    db.close()
    return User(user_email, user[1], user[2], user[3], user[4], user[5], user[6])


def get_user_db_type(user):
    if user.db_type == "SQLite":
        return "SQLite"
    elif user.db_type == "ActiveCampaign":
        return "ActiveCampaign"
    else:
        return "None"


def main_process(email, columns, column_limit, row_limit):
    # client = get_activecampaign_connection(email)
    # input_user_data = get_activecampaign_data(client, columns, column_limit, row_limit)
    input_user_data = get_data(
        "/home/jakes/scratch/automeet-backend/doing_stuff/benDB.db",
        columns,
        column_limit,
        row_limit,
    )
    print(input_user_data)
    gpt_output = chat_with_gpt(input_user_data)
    print(gpt_output)
    send_email(email, gpt_output)


def run_main_process():
    # for email in emails in db where they have a subscription
    columns = [
        "ID",
        "First Name",
        "Last Name",
        "*Mgmt Notes",
        "*Investment Thesis",
        "*Industries",
        "*Interests (Abstract & Ideas)",
        "*Background",
        "*What do you hope to gain?",
        "*Current Focus",
        "*Application Answer",
        "*Expertise",
    ]
    column_limit = 11
    row_limit = 200
    for email in ["jakespvk@gmail.com"]:
        main_process(email, columns, column_limit, row_limit)


# run_main_process()


def run_scheduler():
    schedule.every().day.at("22:12").do(run_main_process)
    while True:
        schedule.run_pending()


# scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
# scheduler_thread.start()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://automeet.space",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/signin/")
async def sign_in(data: EmailRequest):
    token = create_magic_link_token(data.email)
    user = get_user(data.email)
    user.login_token = token
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET login_token = ? WHERE email = ?",
        (token, data.email),
    )
    db.commit()
    db.close()
    send_magic_link(data.email, token)
    return {"message": "Magic link sent to your email!"}


@app.get("/verify")
async def verifyLogin(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        print(payload)
        return {"email": f"{email}", "token": token, "message": "Login successful!"}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")


@app.get("/dashboard/{email}/{token}")
async def dashboard(email: str, token: str):
    user = get_user(email)
    print(user.db_type)
    if user.login_token == token:
        return {"email": user.email, "db_type": get_user_db_type(user)}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
