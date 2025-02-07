import sqlite3
from activecampaign.client import Client


def get_db_credentials(email) -> (str, str):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT activatecampaign_api_key, activecampaign_api_url FROM users WHERE email = '{email}'"
    )
    api_key = cursor.fetchone()[0]
    api_url = cursor.fetchone()[1]
    conn.close()
    return api_key, api_url


def get_activecampaign_connection(email) -> Client:
    activecampaign_api_key, activecampaign_api_url = get_db_credentials(email)
    return Client(api_key=activecampaign_api_key, server_url=activecampaign_api_url)


def get_activecampaign_data(
    client: Client, columns: [], column_limit: int, row_limit: int
) -> str:
    return client.contacts.list_all_contacts()
