import requests
import sqlite3


def get_db_credentials(email) -> (str, str):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT api_url, api_key FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    api_url = result[0]
    api_key = result[1]
    conn.close()
    return api_url, api_key


def get_contacts(email):
    api_url, api_key = get_db_credentials(email)
    url = f"{api_url}/api/3/contacts"
    headers = {
        "accept": "application/json",
        "Api-Token": api_key,
    }
    response = requests.get(url, headers=headers)
    contacts = response.json().get("contacts")
    contacts_parsed = []
    for contact in contacts:
        custom_fields = get_custom_fields(contact.get("id"), api_url, api_key)
        contacts_parsed.append(
            (
                contact.get("id"),
                contact.get("firstName"),
                contact.get("lastName"),
                contact.get("email"),
                custom_fields,
            )
        )
    return contacts_parsed


def get_fields(email):
    api_url, api_key = get_db_credentials(email)
    fields = ["id", "firstName", "lastName", "email"]
    url = f"{api_url}/api/3/fields"
    headers = {
        "accept": "application/json",
        "Api-Token": api_key,
    }
    response = requests.get(url, headers=headers)
    for field in response.json().get("fields"):
        fields.append(field.get("title"))
    return fields


def get_custom_fields(id, email):
    api_url, api_key = get_db_credentials(email)
    url = f"{api_url}/api/3/contacts/{id}/fieldValues"
    headers = {
        "accept": "application/json",
        "Api-Token": api_key,
    }
    response = requests.get(url, headers=headers)
    if response.json().get("fieldValues") == []:
        return []
    else:
        custom_field_responses = []
        for field in response.json().get("fieldValues"):
            custom_field_responses.append(field.get("value"))
        return custom_field_responses
