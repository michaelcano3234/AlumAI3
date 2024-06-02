import sqlite3

def get_column_info(table_name):
    conn = sqlite3.connect('dataset_alumni.db')
    cursor = conn.cursor()

    # Fetch column information using PRAGMA
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    # Print column information
    for column in columns:
        name = column[1]
        data_type = column[2]
        print(f"{name}: {data_type}")


get_column_info("test_alumni")
