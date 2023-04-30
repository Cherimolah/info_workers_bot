import sqlite3


def get_connection():
    db = sqlite3.connect("database.sqlite3", timeout=999)
    cursor = db.cursor()
    return db, cursor


def create_schema():
    db, cursor = get_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS items(id INTEGER PRIMARY KEY, "
                   "name TEXT Unique, count INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY ,"
                   "screen_name TEXT, full_name TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY,"
                   "user_id INTEGER, item_id INTEGER, alteration INTEGER, created_at DATETIME,"
                   "FOREIGN KEY (user_id) REFERENCES users(user_id),"
                   " FOREIGN KEY (item_id) REFERENCES items(id))")
    db.commit()


create_schema()

