import sqlite3
import schedule
import threading

from typing import List  # Annotated
from pydantic import BaseModel, EmailStr

from db_providers.active_campaign_adapter import get_contacts
# from db_providers.sqlite_adapter import get_data

from query_gpt import chat_with_gpt
from send_result_email import send_email


class EmailRequest(BaseModel):
    email: EmailStr


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
            poll_frequency=poll_frequency,
        )


def get_subscription_users():
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE subscription = 1")
    users = cursor.fetchall()
    db.close()
    return users


def get_user(user_email):
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (user_email,),
    )
    user = cursor.fetchone()
    db.close()
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


def process_function(column_limit, row_limit):
    # TODO: validation for column and row limits and poll_frequency
    subscription_users = get_subscription_users()
    for user in subscription_users:
        ## get users data
        # should maybe create another user constructor so this is possible
        #    User(user)
        # instead of running all the logic in get_user again
        # TODO: Dedupe
        user = get_user(user[0])
        ## query activecampaign
        # TODO: fix get only active columns
        contacts = get_contacts(user.email)
        ## compose the prompt
        # TODO: fix this...... update: fixed??
        prompt = ""
        for i in range(min(row_limit, len(contacts))):
            if len(contacts[i]) < column_limit:
                current_contact = ""
                for j in range(min(column_limit, len(contacts[i]))):
                    current_contact = current_contact + str(contacts[i][j])
                prompt = prompt + current_contact + "\n"
            else:
                prompt = prompt + str(contacts[i]) + "\n"
        ## send the prompt to gpt
        gpt_output = chat_with_gpt(prompt)
        ## send email result
        send_email(user.email, gpt_output)

    # client = get_activecampaign_connection(email)
    # input_user_data = get_activecampaign_data(client, columns, column_limit, row_limit)
    # input_user_data = get_data(
    #     "/home/jakes/scratch/automeet-backend/doing_stuff/benDB.db",
    #     columns,
    #     column_limit,
    #     row_limit,
    # )
    # print(input_user_data)
    # gpt_output = chat_with_gpt(input_user_data)
    # print(gpt_output)
    # send_email(email, gpt_output)


def run_process_function():
    # for email in emails in db where they have a subscription
    # columns = get_fields("jakespvk@gmail.com")
    # columns = [
    #     "ID",
    #     "First Name",
    #     "Last Name",
    #     "*Mgmt Notes",
    #     "*Investment Thesis",
    #     "*Industries",
    #     "*Interests (Abstract & Ideas)",
    #     "*Background",
    #     "*What do you hope to gain?",
    #     "*Current Focus",
    #     "*Application Answer",
    #     "*Expertise",
    # ]
    column_limit = 11
    row_limit = 200
    process_function(column_limit, row_limit)


# run_main_process()


def test_function():
    send_email("jakespvk@gmail.com", "test")
    print("success sent email")


def run_scheduler():
    # schedule.every().day.at("22:12").do(run_process_function)
    schedule.every(1).minutes.do(run_process_function)
    while True:
        schedule.run_pending()


def __main__():
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()


if __name__ == "__main__":
    __main__()
