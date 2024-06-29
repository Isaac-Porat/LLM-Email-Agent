import sqlite3
import os
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

class EmailDatabase:
    def __init__(self, db_name='emails.db'):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, db_name)
        self.conn = sqlite3.connect(db_path)
        print(f"Database created/connected at: {db_path}")

    def table_exists(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='emails'
        ''')
        return cursor.fetchone() is not None

    def upsert_email(self, sender, body, sent_date):
        if not self.table_exists():
            raise ValueError("The 'emails' table does not exist. Please create it first.")

        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO emails (sender, body, sent_date)
        VALUES (?, ?, ?)
        ON CONFLICT(sender, sent_date)
        DO UPDATE SET body = excluded.body
        ''', (sender, body, sent_date))
        self.conn.commit()

    def get_all_emails(self):
        if not self.table_exists():
            return []

        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM emails ORDER BY sent_date DESC')
        return cursor.fetchall()

    def close(self):
        self.conn.close()