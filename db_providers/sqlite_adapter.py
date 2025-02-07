import sqlite3


def get_db_path(email) -> (str, str):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT db_path FROM users WHERE email = '{email}'")
    db_path = cursor.fetchone()[0]
    conn.close()
    return db_path


def get_data(db_path: str, columns: [], column_limit: int, row_limit: int) -> str:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    columns_str = ""
    for column in columns:
        if " " in column:
            columns_str += f""""{column}", """
        elif "*" in column:
            columns_str += f""""{column}", """
        else:
            columns_str += f"{column}, "
    columns_str = columns_str[:-2]
    cursor.execute(f"SELECT {columns_str} FROM client_table LIMIT {row_limit}")
    data_rows = cursor.fetchall()
    conn.close()
    data_str = ""
    for data_row in data_rows:
        for i, column in enumerate(columns):
            if i == len(columns) - 1:
                data_str = data_str + f"{column}: {data_row[i]}"
            else:
                data_str = data_str + f"{column}: {data_row[i]}, "
        data_str = data_str + "\n"
    return data_str
