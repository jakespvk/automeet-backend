import sqlite3
from activecampaign.client import Client


def get_db_credentials(email) -> (str, str):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT api_url, api_key FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    api_url = result[0]
    api_key = result[1]
    conn.close()
    return api_url, api_key


def get_activecampaign_connection(email) -> Client:
    activecampaign_api_url, activecampaign_api_key = get_db_credentials(email)
    return Client(activecampaign_api_url, activecampaign_api_key)


def get_activecampaign_data(
    client: Client, columns: [], column_limit: int, row_limit: int
) -> str:
    return client.contacts.list_all_contacts()
