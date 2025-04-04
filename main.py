import sqlite3

from main_process import __main__
from db_helper_functions import db_remove_provider

from typing import List, Optional  # Annotated

import db_providers.active_campaign_adapter
import db_providers.attio_adapter

import subprocess

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
TOKEN_EXPIRE_MINUTES = 60


class EmailRequest(BaseModel):
    email: EmailStr


class SetupSubscription(BaseModel):
    email: EmailStr
    db_type: str
    api_url: Optional[str] = ""
    api_key: Optional[str] = ""
    attio_token: Optional[str] = ""


class User(BaseModel):
    email: EmailStr
    subscription: bool
    db_type: str
    columns: List
    active_columns: List
    column_limit: int
    row_limit: int
    login_token: str
    api_url: str
    api_key: str
    attio_token: str
    poll_frequency: str

    def __init__(
        self,
        email: EmailStr,
        subscription: bool = False,
        db_type: str = "",
        columns: List = [],
        active_columns: List = [],
        column_limit: int = 0,
        row_limit: int = 0,
        login_token: str = "",
        api_url: str = "",
        api_key: str = "",
        attio_token: str = "",
        poll_frequency: str = "",
    ) -> None:
        super().__init__(
            email=email,
            subscription=subscription,
            db_type=db_type,
            columns=columns,
            active_columns=active_columns,
            column_limit=column_limit,
            row_limit=row_limit,
            login_token=login_token,
            api_url=api_url,
            api_key=api_key,
            attio_token=attio_token,
            poll_frequency=poll_frequency,
        )


class UpdateUser(BaseModel):
    user: User


def setup_subscription_helper(email, db_type, api_url="", api_key="", attio_token=""):
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    if len(api_key) > 0:
        cursor.execute(
            f"UPDATE users SET db_type = '{db_type}', api_url = '{api_url}', api_key = '{api_key}' WHERE email = '{email}'"
        )
    elif len(attio_token) > 0:
        cursor.execute(
            f"UPDATE users SET db_type = '{db_type}', attio_token = '{attio_token}' WHERE email = '{email}'"
        )
    else:
        return
    db.commit()
    db.close()
    user = get_user(email)
    if user.db_type == "ActiveCampaign":
        user.columns = db_providers.active_campaign_adapter.get_fields(email)
    elif user.db_type == "Attio":
        user.columns = db_providers.attio_adapter.get_fields(email)
    update_user_db_fields(user)
    user.active_columns = user.columns[0:4]
    update_user_db_details(user)


def update_user_db_fields(user: User):
    if user.columns == []:
        columns_str = ""
    else:
        columns_str = ",".join(user.columns)
    if user.db_type == "ActiveCampaign":
        query = f"UPDATE users \
            SET columns = '{columns_str}' \
            WHERE email = '{user.email}'"
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def update_user_db_details(user: User):
    if user.active_columns == []:
        active_columns_str = ""
    else:
        active_columns_str = ",".join(user.active_columns)
    if user.db_type == "SQLite":
        query = f"UPDATE users \
            SET api_url = '{user.api_url}', \
            api_key = '{user.api_key}', \
            active_columns = '{active_columns_str}', \
            poll_frequency = '{user.poll_frequency}' \
            WHERE email = '{user.email}'"
    elif user.db_type == "ActiveCampaign":
        query = f"UPDATE users \
            SET api_url = '{user.api_url}', \
            api_key = '{user.api_key}', \
            active_columns = '{active_columns_str}', \
            poll_frequency = '{user.poll_frequency}' \
            WHERE email = '{user.email}'"
    elif user.db_type == "Attio":
        query = f"UPDATE users \
            SET attio_token = '{user.attio_token}', \
            active_columns = '{active_columns_str}', \
            poll_frequency = '{user.poll_frequency}' \
            WHERE email = '{user.email}'"
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()


def create_magic_link_token(email: str) -> str:
    expiration = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expiration}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def send_magic_link(email: str, token: str):
    process = subprocess.run("hostname", shell=True, capture_output=True, text=True)
    if "ubuntu" in process.stdout.strip():
        base_url = "https://automeet.space"
    else:
        base_url = "http://localhost:3000"
    magic_link = f"{base_url}/magic?token={token}"
    msg = MIMEText(f"Click this link to log in: {magic_link}")
    msg["Subject"] = "Your magic link login"
    msg["From"] = "Automeet"
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.send_message(msg)


def new_user(user: User) -> User:
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (email, subscription, db_type, columns, active_columns, column_limit, row_limit, login_token, api_url, api_key, poll_frequency) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            user.email,
            user.subscription,
            user.db_type,
            ",".join(user.columns),
            ",".join(user.active_columns),
            user.column_limit,
            user.row_limit,
            user.login_token,
            user.api_url,
            user.api_key,
            user.attio_token,
            user.poll_frequency,
        ),
    )
    db.commit()
    db.close()
    return user


def get_user(user_email) -> User:
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (user_email,),
    )
    user = cursor.fetchone()
    db.close()
    if user is None:
        return new_user(User(user_email))
    if user[3] == "":
        list_columns = []
    else:
        list_columns = user[3].split(",")
    if user[9] == "":
        list_active_columns = []
    else:
        list_active_columns = user[9].split(",")
    return User(
        user[0],
        user[1] or False,
        user[2] or "",
        list_columns or [],
        list_active_columns or [],
        user[4] or 0,
        user[5] or 0,
        user[6] or "",
        user[7] or "",
        user[8] or "",
        user[10] or "",
    )


def get_user_db_type(user):
    if user.db_type == "SQLite":
        return "SQLite"
    elif user.db_type == "ActiveCampaign":
        return "ActiveCampaign"
    else:
        return "None"


def set_user_token(user, token):
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "UPDATE users SET login_token = ? WHERE email = ?",
        (token, user.email),
    )
    db.commit()
    db.close()


app = FastAPI()
__main__()

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
    set_user_token(get_user(data.email), token)
    send_magic_link(data.email, token)
    return {"message": "Magic link sent to your email!"}


@app.post("/auth/signup/")
async def sign_up(data: EmailRequest):
    token = create_magic_link_token(data.email)
    user = User(data.email)
    new_user(user)
    set_user_token(user, token)
    send_magic_link(user.email, token)
    return {"message": "Magic link sent to your email!"}


@app.get("/verify")
async def verifyLogin(token: str = Query(...)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user(email)
        if user.login_token == token:
            return {"user": user}
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")


@app.post("/set-user-db-details")
async def set_user_db_details(data: UpdateUser):
    update_user_db_details(data.user)
    return {"message": "User details updated!", "user": get_user(data.user.email)}


@app.post("/setup-subscription/ActiveCampaign")
async def setup_subscription_activecampaign(data: SetupSubscription):
    print("here in setup ac")
    try:
        setup_subscription_helper(
            email=data.email,
            db_type="ActiveCampaign",
            api_url=data.api_url,
            api_key=data.api_key,
        )
    except:  # noqa: E722
        return {"message": "Error setting up subscription"}
    return {"message": "Subscription setup successful!"}


@app.post("/setup-subscription/Attio")
async def setup_subscription_attio(data: SetupSubscription):
    try:
        setup_subscription_helper(
            email=data.email, db_type="Attio", attio_token=data.attio_token
        )
    except:  # noqa: E722
        return {"message": "Error setting up subscription"}
    return {"message": "Subscription setup successful!"}


@app.delete("/provider/{email}")
async def remove_provider(email: EmailStr):
    try:
        db_remove_provider(email)  # noqa: F405
    except:  # noqa: E722
        return {"message": "Error updating db"}
    return {"message": "DB provider removed"}


@app.get("/automeetbackend")
async def home():
    return {"message": "Hello from Automeet Backend"}
