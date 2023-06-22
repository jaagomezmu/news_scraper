import sqlite3
import os


def create_db():
    data_dir = os.path.join(os.path.abspath(os.path.join(os.getcwd(), os.pardir)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    db_path = os.path.join(data_dir, 'urls.db')

    db = sqlite3.connect(db_path)
    cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            processed BOOLEAN DEFAULT 0
        )
    """)

    cursor.close()
    db.close()


if __name__ == '__main__':
    create_db()

