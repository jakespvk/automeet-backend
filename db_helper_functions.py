import sqlite3


def db_remove_provider(email):
    db = sqlite3.connect("user.db")
    cursor = db.cursor()
    cursor.execute(f"UPDATE users SET db_type = '' WHERE email = '{email}'")
    db.commit()
    db.close()
