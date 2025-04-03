import requests
import sqlite3


def get_db_credentials(email) -> (str, str):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT attio_token FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    attio_token = result[0]
    conn.close()
    return attio_token


def get_contacts(email):
    attio_token = get_db_credentials(email)
    url = "https://api.attio.com/v2/objects/people/records/query"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "Bearer " + attio_token,
    }
    response = requests.post(url, headers=headers)
    return response.text


def get_fields(email):
    attio_token = get_db_credentials(email)
    url = "https://api.attio.com/v2/objects/identifier/attributes"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer " + attio_token,
    }
    response = requests.get(url, headers=headers)
    return response.text
